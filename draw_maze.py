from mlx.mlx import Mlx

mlx = Mlx()

mlx_ptr = mlx.mlx_init()
win_ptr = mlx.mlx_new_window(mlx_ptr, 800, 600, "Maze window")
mlx.mlx_pixel_put(mlx_ptr, win_ptr, 200, 200, 0xFFFFFF)

mlx.mlx_loop(mlx_ptr)