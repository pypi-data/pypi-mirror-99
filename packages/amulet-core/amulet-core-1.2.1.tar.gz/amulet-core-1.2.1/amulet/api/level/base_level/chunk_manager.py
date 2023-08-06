from typing import Optional, Tuple, Generator, Set, TYPE_CHECKING
import os
import shutil
import weakref

from amulet.api.data_types import DimensionCoordinates, Dimension
from amulet.api.chunk import Chunk
from amulet.api.history.data_types import EntryType, EntryKeyType
from amulet.api.history.base import RevisionManager
from amulet.api.history.revision_manager import DiskRevisionManager
from amulet.api.errors import ChunkDoesNotExist, ChunkLoadError
from amulet.api.history.history_manager import DatabaseHistoryManager
from amulet.api.cache import get_cache_db

if TYPE_CHECKING:
    from amulet.api.level import BaseLevel


class ChunkDiskEntry(DiskRevisionManager):
    __slots__ = ("_world",)

    def __init__(self, world: "BaseLevel", directory: str, initial_state: EntryType):
        self._world = weakref.ref(world)
        super().__init__(directory, initial_state)

    @property
    def world(self) -> "BaseLevel":
        return self._world()

    def _serialise(self, path: str, entry: Optional[Chunk]) -> Optional[str]:
        if entry is None:
            return None
        else:
            pickled_bytes = entry.pickle()
            get_cache_db().put(path.encode("utf-8"), pickled_bytes)
            return path

    def _deserialise(self, path: Optional[str]) -> Optional[Chunk]:
        if path is None:
            return None
        else:
            pickled_bytes = get_cache_db().get(path.encode("utf-8"))
            return Chunk.unpickle(
                pickled_bytes, self.world.block_palette, self.world.biome_palette
            )


class ChunkManager(DatabaseHistoryManager):
    """The ChunkManager class is a class that handles chunks within a world.
    It handles the temporary database of chunks in RAM that can be directly modified.
    It handles a serialised version of the chunks on disk to reduce RAM usage.
    It also contains a history manager to allow undoing and redoing of changes."""

    DoesNotExistError = ChunkDoesNotExist
    LoadError = ChunkLoadError

    def __init__(self, temp_dir: str, world: "BaseLevel"):
        super().__init__()
        self._temp_dir: str = temp_dir  # the location to serialise Chunks to
        shutil.rmtree(self._temp_dir, ignore_errors=True)
        self._world = weakref.ref(world)

    @property
    def world(self) -> "BaseLevel":
        return self._world()

    def changed_chunks(self) -> Generator[DimensionCoordinates, None, None]:
        """The location of every chunk that has been changed since the last save."""
        yield from self.changed_entries()

    def unload(self, safe_area: Optional[Tuple[Dimension, int, int, int, int]] = None):
        """Unload all chunks not in the safe area from the temporary database
        Safe area format: dimension, min chunk X|Z, max chunk X|Z"""
        with self._lock:
            if safe_area is None:
                self._temporary_database.clear()
            else:
                unload_chunks = []
                dimension, minx, minz, maxx, maxz = safe_area
                for (cd, cx, cz), chunk in self._temporary_database.items():
                    if not (
                        cd == dimension and minx <= cx <= maxx and minz <= cz <= maxz
                    ):
                        unload_chunks.append((cd, cx, cz))
                for chunk_key in unload_chunks:
                    del self._temporary_database[chunk_key]

    def unload_unchanged(self):
        """Unload all chunks that have not been marked as changed."""
        with self._lock:
            unchanged = []
            for key, chunk in self._temporary_database.items():
                if not chunk.changed:
                    unchanged.append(key)
            for key in unchanged:
                del self._temporary_database[key]

    def has_chunk(self, dimension: Dimension, cx: int, cz: int) -> bool:
        """Does the ChunkManager have the chunk specified"""
        return self._has_entry(
            (dimension, cx, cz)
        ) or self.world.level_wrapper.has_chunk(cx, cz, dimension)

    def __contains__(self, item: DimensionCoordinates):
        return self._has_entry(item)

    def all_chunk_coords(self, dimension: Dimension) -> Set[Tuple[int, int]]:
        """The coordinates of every chunk in this world.
        This is the combination of chunks saved to the world and chunks yet to be saved."""
        with self._lock:
            coords = set()
            deleted_chunks = set()
            for dim, cx, cz in self._temporary_database.keys():
                if dim == dimension:
                    if self._temporary_database[(dim, cx, cz)] is None:
                        deleted_chunks.add((cx, cz))
                    else:
                        coords.add((cx, cz))

            for dim, cx, cz in self._history_database.keys():
                if dim == dimension and (dim, cx, cz) not in self._temporary_database:
                    if self._history_database[(dim, cx, cz)].is_deleted:
                        deleted_chunks.add((cx, cz))
                    else:
                        coords.add((cx, cz))

            for cx, cz in self.world.level_wrapper.all_chunk_coords(dimension):
                if (cx, cz) not in coords and (cx, cz) not in deleted_chunks:
                    coords.add((cx, cz))

        return coords

    def get_chunk(self, dimension: Dimension, cx: int, cz: int) -> Optional[Chunk]:
        """
        Gets the chunk object at the specified chunk coordinates.
        This may be a Chunk instance if the chunk exists, None if it is known to not exist
        or ChunkDoesNotExist will be raised if there is no record so it is unknown if it exists or not.
        Use has_chunk to check if there is a record of the chunk.

        :param dimension: The dimension to get the chunk from
        :param cx: The X coordinate of the desired chunk
        :param cz: The Z coordinate of the desired chunk
        :return: A Chunk instance or None
        :raises:
            ChunkDoesNotExist: If the chunk does not exist (was deleted or never created)
        """
        return self._get_entry((dimension, cx, cz))

    def put_chunk(self, chunk: Chunk, dimension: Dimension):
        """Add a chunk to the universal world database"""
        chunk.block_palette = self.world.block_palette
        chunk.biome_palette = self.world.biome_palette
        self._put_entry((dimension, chunk.cx, chunk.cz), chunk)

    def delete_chunk(self, dimension: Dimension, cx: int, cz: int):
        """Delete a chunk from the universal world database"""
        self._delete_entry((dimension, cx, cz))

    def _get_entry_from_world(self, key: EntryKeyType) -> EntryType:
        dimension, cx, cz = key
        chunk = self.world.level_wrapper.load_chunk(cx, cz, dimension)
        chunk.block_palette = self.world.block_palette
        chunk.biome_palette = self.world.biome_palette
        return chunk

    def _create_new_revision_manager(
        self, key: EntryKeyType, original_entry: EntryType
    ) -> RevisionManager:
        dimension, cx, cz = key
        directory = os.path.join(self._temp_dir, str(dimension), f"{cx}.{cz}")
        return ChunkDiskEntry(self.world, directory, original_entry)
