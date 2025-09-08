from ultralytics import YOLO

def run_diagnostic_test():
    """
    This test uses ONLY official, built-in components from Ultralytics
    to verify if the environment, PyTorch, and CUDA are working correctly.
    It does not use any of your local data.
    """
    print("\n" + "="*50)
    print("🚀 Starting a diagnostic test with the official coco128 dataset.")
    print("This will test your environment from scratch.")
    print("="*50 + "\n")

    try:
        # 1. Load a standard model. It will be downloaded if not present.
        # We use 'n' model for the quickest possible test.
        model = YOLO('yolov8n.pt')

        # 2. Train on the standard coco128 dataset.
        # YOLO will handle downloading and setting up this dataset automatically.
        # We only train for 3 epochs because we just need to see if it starts.
        results = model.train(
            data='coco128.yaml',   # Official dataset config
            epochs=3,             # Just a few epochs to test
            imgsz=320,            # Small image size for speed
            device=0,             # Use a single GPU
            name='coco128_diagnostic_run' # Name for the results folder
        )

        print("\n" + "="*50)
        print("✅ SUCCESS! The diagnostic test completed.")
        print("This means your environment (PyTorch, CUDA, Ultralytics) is working correctly.")
        print("The problem is likely related to your custom dataset or .yaml file.")
        print("="*50 + "\n")

    except Exception as e:
        print("\n" + "="*50)
        print(f"🔥 FAILURE! The diagnostic test failed with an error: {e}")
        print("This suggests a deeper issue with your environment, not your data.")
        print("="*50 + "\n")


if __name__ == '__main__':
    run_diagnostic_test()