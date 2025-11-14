# core/world.py
# Chunked city generator with meters-aware parameters.
import pygame
import threading
import time
import random
import math
import collections
from settings import METERS_PER_TILE  # para convertir metros -> tiles si se pasan parámetros en metros

# Tile constants (city)
TILE_EMPTY = 0
TILE_ROAD = 1
TILE_SIDEWALK = 2
TILE_BIKE = 3
TILE_BUILDING = 4
TILE_PARK = 5
TILE_WATER = 6
TILE_PLAZA = 7

TILE_COLORS = {
    TILE_EMPTY: (180, 200, 150),
    TILE_ROAD: (60, 60, 70),
    TILE_SIDEWALK: (200, 200, 200),
    TILE_BIKE: (80, 200, 160),
    TILE_BUILDING: (120, 120, 120),
    TILE_PARK: (70, 160, 70),
    TILE_WATER: (70, 130, 180),
    TILE_PLAZA: (200, 180, 140),
}

SOLID_TILES = {TILE_BUILDING, TILE_WATER}

CHUNK_SIZE = 16
CACHE_RADIUS_CHUNKS = 4
MAX_CACHE_CHUNKS = 9 * 9

class Chunk:
    def __init__(self, cx, cy, tiles):
        self.cx = cx
        self.cy = cy
        self.tiles = tiles
        self.timestamp = time.time()

class World:
    def __init__(self, mapa=None, tile_size=32, seed=12345,
                 major_spacing=None, minor_spacing=None,
                 major_spacing_meters=None, minor_spacing_meters=None,
                 major_road_width=3, minor_road_width=1,
                 sidewalk_width=1, bike_lane_width=1):
        """
        Ahora aceptamos major_spacing_meters / minor_spacing_meters en metros.
        Si se pasan, convertimos a tiles usando METERS_PER_TILE desde settings.
        """
        self.mapa = mapa
        self.tile_size = tile_size
        self.seed = int(seed) & 0xFFFFFFFF

        rng0 = random.Random(self.seed ^ 0x9E3779B97F4A7C15)

        # Convert meters->tiles if meters params provided
        if major_spacing_meters is not None:
            calc_major = max(4, int(round(major_spacing_meters / METERS_PER_TILE)))
            self.major_spacing = calc_major
        else:
            self.major_spacing = major_spacing or rng0.randint(24, 48)

        if minor_spacing_meters is not None:
            calc_minor = max(4, int(round(minor_spacing_meters / METERS_PER_TILE)))
            self.minor_spacing = calc_minor
        else:
            self.minor_spacing = minor_spacing or rng0.randint(8, 16)

        self.major_road_width = max(1, int(major_road_width))
        self.minor_road_width = max(1, int(minor_road_width))
        self.sidewalk_width = max(0, int(sidewalk_width))
        self.bike_lane_width = max(0, int(bike_lane_width))

        # random offsets
        self.major_offset_x = rng0.randint(0, self.major_spacing - 1)
        self.major_offset_y = rng0.randint(0, self.major_spacing - 1)
        self.minor_offset_x = rng0.randint(0, self.minor_spacing - 1)
        self.minor_offset_y = rng0.randint(0, self.minor_spacing - 1)

        # spawn protection
        self.spawn_protect_center = None
        self.spawn_protect_radius_tiles = 10

        # chunk caches
        self.chunks = {}
        self.chunks_lock = threading.Lock()
        self.to_generate = collections.deque()
        self.to_generate_lock = threading.Lock()

        self._stop_thread = False
        self.worker = threading.Thread(target=self._generator_thread, daemon=True)
        self.worker.start()

    # Worker and other methods unchanged (deterministic city algorithm)
    def _generator_thread(self):
        while not self._stop_thread:
            coord = None
            with self.to_generate_lock:
                if self.to_generate:
                    coord = self.to_generate.popleft()
            if coord is None:
                time.sleep(0.01)
                continue
            cx, cy = coord
            with self.chunks_lock:
                if (cx, cy) in self.chunks:
                    continue
            try:
                chunk = self._generate_chunk(cx, cy)
                with self.chunks_lock:
                    if (cx, cy) not in self.chunks:
                        self.chunks[(cx, cy)] = chunk
                        if len(self.chunks) > MAX_CACHE_CHUNKS:
                            self._evict_oldest()
            except Exception:
                import traceback
                traceback.print_exc()
            time.sleep(0.001)

    def stop(self):
        self._stop_thread = True
        try:
            self.worker.join(timeout=0.5)
        except Exception:
            pass

    def _evict_oldest(self):
        oldest = None
        oldest_time = time.time()
        for k, ch in self.chunks.items():
            if ch.timestamp < oldest_time:
                oldest_time = ch.timestamp
                oldest = k
        if oldest:
            del self.chunks[oldest]

    def set_spawn_protection(self, px, py, radius_tiles=10, coords_in_pixels=True):
        if coords_in_pixels:
            tx = int(px // self.tile_size)
            ty = int(py // self.tile_size)
        else:
            tx = int(px)
            ty = int(py)
        self.spawn_protect_center = (tx, ty)
        self.spawn_protect_radius_tiles = int(radius_tiles)

    def clear_spawn_protection(self):
        self.spawn_protect_center = None

    def _block_rng(self, bx, by):
        h = (self.seed ^ ((bx * 341873128712) & 0xFFFFFFFF) ^ ((by * 132897987541) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return random.Random(h)

    def _is_major_road_at(self, tx):
        return ((tx - self.major_offset_x) % self.major_spacing) < self.major_road_width

    def _is_major_road_at_y(self, ty):
        return ((ty - self.major_offset_y) % self.major_spacing) < self.major_road_width

    def _is_minor_road_at(self, tx):
        return ((tx - self.minor_offset_x) % self.minor_spacing) < self.minor_road_width

    def _is_minor_road_at_y(self, ty):
        return ((ty - self.minor_offset_y) % self.minor_spacing) < self.minor_road_width

    def _chunk_block_coords(self, tx, ty):
        bx = math.floor((tx - self.major_offset_x) / self.major_spacing)
        by = math.floor((ty - self.major_offset_y) / self.major_spacing)
        return bx, by

    def _generate_chunk(self, cx, cy):
        tiles = [[TILE_EMPTY for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]

        for ly in range(CHUNK_SIZE):
            for lx in range(CHUNK_SIZE):
                tx = cx * CHUNK_SIZE + lx
                ty = cy * CHUNK_SIZE + ly

                v_major = self._is_major_road_at(tx)
                h_major = self._is_major_road_at_y(ty)
                v_minor = self._is_minor_road_at(tx)
                h_minor = self._is_minor_road_at_y(ty)

                is_road = False
                if v_major or h_major:
                    is_road = True
                elif v_minor or h_minor:
                    is_road = True

                if is_road:
                    tiles[ly][lx] = TILE_ROAD
                    continue

                bx, by = self._chunk_block_coords(tx, ty)
                rng = self._block_rng(bx, by)

                if self.spawn_protect_center is not None:
                    protect_tx, protect_ty = self.spawn_protect_center
                    block_center_tx = bx * self.major_spacing + (self.major_spacing // 2) + self.major_offset_x
                    block_center_ty = by * self.major_spacing + (self.major_spacing // 2) + self.major_offset_y
                    dist = math.hypot(block_center_tx - protect_tx, block_center_ty - protect_ty)
                    if dist <= self.spawn_protect_radius_tiles:
                        tiles[ly][lx] = TILE_PLAZA if rng.random() < 0.6 else TILE_EMPTY
                        continue

                p = rng.random()
                if p < 0.08:
                    tiles[ly][lx] = TILE_PARK
                    continue
                elif p < 0.12:
                    tiles[ly][lx] = TILE_PLAZA
                    continue
                elif p < 0.14:
                    tiles[ly][lx] = TILE_WATER
                    continue
                else:
                    local_x_in_block = (tx - (bx * self.major_spacing + self.major_offset_x)) % self.major_spacing
                    local_y_in_block = (ty - (by * self.major_spacing + self.major_offset_y)) % self.major_spacing

                    coverage = 0.65 + (rng.random() - 0.5) * 0.2
                    lot_w = self.minor_spacing
                    lot_h = self.minor_spacing

                    lot_x = int(local_x_in_block // lot_w)
                    lot_y = int(local_y_in_block // lot_h)
                    lot_rng = self._block_rng(bx * 7919 + lot_x, by * 48611 + lot_y)

                    lot_roll = lot_rng.random()
                    if lot_roll < coverage:
                        lx_in_lot = int(local_x_in_block % lot_w)
                        ly_in_lot = int(local_y_in_block % lot_h)
                        pad = 1
                        inner_w = max(1, lot_w - pad*2)
                        inner_h = max(1, lot_h - pad*2)
                        if (pad <= lx_in_lot < pad + inner_w) and (pad <= ly_in_lot < pad + inner_h):
                            tiles[ly][lx] = TILE_BUILDING
                        else:
                            tiles[ly][lx] = TILE_EMPTY
                    else:
                        tiles[ly][lx] = TILE_PARK

        # sidewalks / bike lanes adjacency pass
        for ly in range(CHUNK_SIZE):
            for lx in range(CHUNK_SIZE):
                if tiles[ly][lx] == TILE_ROAD:
                    continue
                tx = cx * CHUNK_SIZE + lx
                ty = cy * CHUNK_SIZE + ly
                min_dist = 9999
                for oy in range(- (self.sidewalk_width + self.bike_lane_width + 1), (self.sidewalk_width + self.bike_lane_width + 2)):
                    for ox in range(- (self.sidewalk_width + self.bike_lane_width + 1), (self.sidewalk_width + self.bike_lane_width + 2)):
                        if ox == 0 and oy == 0:
                            continue
                        check_tx = tx + ox
                        check_ty = ty + oy
                        if self._is_major_road_at(check_tx) or self._is_minor_road_at(check_tx) or self._is_major_road_at_y(check_ty) or self._is_minor_road_at_y(check_ty):
                            d = abs(ox) + abs(oy)
                            if d < min_dist:
                                min_dist = d
                threshold = self.sidewalk_width + self.bike_lane_width + 1
                if min_dist <= threshold:
                    if min_dist <= self.bike_lane_width:
                        if tiles[ly][lx] in (TILE_EMPTY, TILE_PARK, TILE_PLAZA):
                            tiles[ly][lx] = TILE_BIKE
                    elif min_dist <= self.bike_lane_width + self.sidewalk_width:
                        if tiles[ly][lx] in (TILE_EMPTY, TILE_PARK, TILE_PLAZA):
                            tiles[ly][lx] = TILE_SIDEWALK

        # smoothing
        for ly in range(1, CHUNK_SIZE-1):
            for lx in range(1, CHUNK_SIZE-1):
                if tiles[ly][lx] == TILE_BUILDING:
                    neighbors = 0
                    for oy in (-1,0,1):
                        for ox in (-1,0,1):
                            if ox == 0 and oy == 0:
                                continue
                            if tiles[ly+oy][lx+ox] == TILE_BUILDING:
                                neighbors += 1
                    if neighbors <= 1:
                        tiles[ly][lx] = TILE_PARK

        return Chunk(cx, cy, tiles)

    def request_chunks_around(self, px, py, radius_chunks=CACHE_RADIUS_CHUNKS):
        center_tx = int(px // self.tile_size)
        center_ty = int(py // self.tile_size)
        center_cx = center_tx // CHUNK_SIZE
        center_cy = center_ty // CHUNK_SIZE

        coords = []
        for cy in range(center_cy - radius_chunks, center_cy + radius_chunks + 1):
            for cx in range(center_cx - radius_chunks, center_cx + radius_chunks + 1):
                coords.append((cx, cy))

        with self.to_generate_lock:
            with self.chunks_lock:
                for coord in coords:
                    if coord not in self.chunks and coord not in self.to_generate:
                        self.to_generate.append(coord)

    def get_chunk(self, cx, cy):
        with self.chunks_lock:
            ch = self.chunks.get((cx, cy))
            if ch:
                ch.timestamp = time.time()
            return ch

    def get_tile(self, tx, ty):
        cx = tx // CHUNK_SIZE
        cy = ty // CHUNK_SIZE
        ch = self.get_chunk(cx, cy)
        if ch is None:
            with self.to_generate_lock:
                if (cx, cy) not in self.to_generate:
                    self.to_generate.append((cx, cy))
            return TILE_EMPTY
        lx = tx - cx * CHUNK_SIZE
        ly = ty - cy * CHUNK_SIZE
        if 0 <= lx < CHUNK_SIZE and 0 <= ly < CHUNK_SIZE:
            return ch.tiles[ly][lx]
        return TILE_EMPTY

    def is_solid_tile(self, tx, ty):
        return self.get_tile(tx, ty) in SOLID_TILES

    def is_area_solid(self, px, py, width, height):
        if width <= 0 or height <= 0:
            return False
        left = int(math.floor(px / self.tile_size))
        top = int(math.floor(py / self.tile_size))
        right = int(math.floor((px + width - 1) / self.tile_size))
        bottom = int(math.floor((py + height - 1) / self.tile_size))
        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                if self.is_solid_tile(tx, ty):
                    return True
        return False

    def is_pixel_solid(self, px, py, check_radius=0):
        tx = int(px // self.tile_size)
        ty = int(py // self.tile_size)
        if check_radius <= 0:
            return self.is_solid_tile(tx, ty)
        offs = int(math.ceil(check_radius / self.tile_size))
        for oy in range(-offs, offs + 1):
            for ox in range(-offs, offs + 1):
                if self.is_solid_tile(tx + ox, ty + oy):
                    return True
        return False

    def draw(self, screen, camera_offset, view_margin_tiles=25):
        cam_x, cam_y = camera_offset
        left = int(math.floor(cam_x / self.tile_size)) - view_margin_tiles
        right = int(math.ceil((cam_x + screen.get_width()) / self.tile_size)) + view_margin_tiles
        top = int(math.floor(cam_y / self.tile_size)) - view_margin_tiles
        bottom = int(math.ceil((cam_y + screen.get_height()) / self.tile_size)) + view_margin_tiles

        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                t = self.get_tile(tx, ty)
                color = TILE_COLORS.get(t, TILE_COLORS[TILE_EMPTY])
                rect = pygame.Rect(tx * self.tile_size - cam_x, ty * self.tile_size - cam_y, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)