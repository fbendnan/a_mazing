from mlx.mlx import Mlx
import sys

mlx = Mlx()

mlx_ptr = mlx.mlx_init()
win_ptr = mlx.mlx_new_window(mlx_ptr, 800, 600, "Maze window")

mlx.mlx_pixel_put(mlx_ptr, win_ptr, 200, 200, 0xFFFFFF)

try:
    mlx.mlx_loop(mlx_ptr)
except KeyboardInterrupt:
    print("Program stopped")
    sys.exit(0)
