import math
from PIL import Image
from app.core.config import MAP_SIZE, OUTPUT_DIR

class BinaryVisualizer:
    """Responsible for generating binary visualizations of files."""

    def __init__(self, map_size: int = MAP_SIZE):
        self.map_size = map_size

    def generate_visualization(self, file_path: str, output_name: str) -> str:
        data = self._read_binary_file(file_path)
        matrix = self._generate_matrix(data)
        image = self._create_image(matrix)
        output_path = OUTPUT_DIR / f"{output_name}.png"
        image.save(output_path)
        return str(output_path)

    def _read_binary_file(self, file_path: str) -> list[int]:
        bytes_list = []
        with open(file_path, "rb") as f:
            while byte := f.read(1):
                # bytes_list.append(int.from_bytes(byte)) <---ON WIN os
                 bytes_list.append(int.from_bytes(byte,'little'))

        return bytes_list

    def _generate_matrix(self, data: list[int]) -> list[list[int]]:
        matrix = [[0] * self.map_size for _ in range(self.map_size)]
        for i in range(len(data) - 1):
            x, y = data[i], data[i + 1]
            if x < self.map_size and y < self.map_size:
                matrix[x][y] += 1
        return matrix

    def _create_image(self, matrix: list[list[int]]) -> Image:
        image = Image.new("RGB", (self.map_size, self.map_size))
        max_val = max((math.log(v) for row in matrix for v in row if v > 0), default=1)
        for i in range(self.map_size):
            for j in range(self.map_size):
                if matrix[i][j] != 0:
                    intensity = int((math.log(matrix[i][j]) / max_val) * 255)
                    image.putpixel((i, j), (intensity, intensity, intensity))
        return image
