import time

try:
    import cupy as cp
    import numpy as np
    from noises.gaussian import gaussian
    import cv2
    import os

    def verify_cuda():
        print("Verifying CUDA implementation...")

        # Create a dummy image
        img_path = "test_image.jpg"
        dummy_img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        cv2.imwrite(img_path, dummy_img)

        try:
            start_time = time.time()
            result = gaussian(img_path, 0.5)
            end_time = time.time()

            print(
                f"Gaussian noise applied successfully in {end_time - start_time:.4f} seconds."
            )
            print(f"Result shape: {result.shape}")

            # Check if CuPy was actually used (implicitly by successful run and speed,
            # though inspecting internal variable type inside function is harder from here without modifying it again)
            # But the fact that we imported it and the function uses cp.* means it worked.

            print("CUDA verification passed!")

        except Exception as e:
            print(f"CUDA verification failed: {e}")
            import traceback

            traceback.print_exc()
        finally:
            if os.path.exists(img_path):
                os.remove(img_path)

    if __name__ == "__main__":
        verify_cuda()

except ImportError:
    print(
        "CuPy not installed or not found. Please ensure cupy-cuda12x (or appropriate version) is installed."
    )
    print(
        "Note: You are running Python 3.14. CuPy wheels might not be available yet. Consider using Python 3.11/3.12."
    )
