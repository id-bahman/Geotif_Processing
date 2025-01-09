import rasterio
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, Entry, filedialog
import os

class GeoTIFFProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoTIFF Image Processor")

        # Label for displaying selected file path
        self.label = Label(root, text="No file selected", wraplength=300)
        self.label.pack(pady=10)

        # Button to open file dialog
        self.open_button = Button(root, text="Open GeoTIFF File", command=self.open_file)
        self.open_button.pack(pady=5)

        # Label for the formula input
        self.formula_label = Label(root, text="Enter formula (e.g., B1 > 100):")
        self.formula_label.pack(pady=10)

        # Entry widget for formula input
        self.formula_entry = Entry(root, width=50)
        self.formula_entry.pack(pady=5)

        # Button to process the image
        self.process_button = Button(root, text="Process Image", command=self.process_image)
        self.process_button.pack(pady=5)

        # Button to save the processed image
        self.save_button = Button(root, text="Save Processed Image", command=self.save_processed_image, state="disabled")
        self.save_button.pack(pady=5)

        self.processed_image = None  # Store the processed image for saving

    def open_file(self):
        # File dialog to select a file
        file_path = filedialog.askopenfilename(title="Select a GeoTIFF file", filetypes=[("GeoTIFF files", "*.tif"), ("All files", "*.*")])
        
        if file_path:
            self.label.config(text=file_path)  # Display the file path
            self.file_path = file_path  # Store the selected file path

    def process_image(self):
        if hasattr(self, 'file_path'):
            try:
                # Open the GeoTIFF file
                with rasterio.open(self.file_path) as dataset:
                    # Read the image data into B1
                    B1 = dataset.read(1)  # Read the first band into B1

                    # Get formula from the entry widget
                    user_formula = self.formula_entry.get()
                    if user_formula:
                        # Apply the formula using eval
                        self.processed_image = eval(user_formula)

                        # Convert boolean to integer or float (True -> 1, False -> 0)
                        self.processed_image = self.processed_image.astype('float32')

                        # Plot the processed image using matplotlib
                        plt.imshow(self.processed_image, cmap='gray')
                        plt.colorbar()
                        plt.title('Processed GeoTIFF Image')
                        plt.show()

                        # Enable the save button after processing
                        self.save_button.config(state="normal")

                    else:
                        print("No formula entered.")
            except Exception as e:
                print(f"Error processing the file: {e}")
        else:
            print("No file selected.")

    def save_processed_image(self):
        if self.processed_image is not None:
            try:
                # Open the original GeoTIFF file to get metadata (CRS, transform)
                with rasterio.open(self.file_path) as dataset:
                    # Define the path for saving the processed image
                    save_path = self.file_path.replace('.tif', '_processed.tif')
                    
                    # Save the processed image as GeoTIFF with original CRS and transform
                    with rasterio.open(
                        save_path, 'w',
                        driver='GTiff',
                        height=self.processed_image.shape[0],
                        width=self.processed_image.shape[1],
                        count=1,
                        dtype=self.processed_image.dtype,
                        crs=dataset.crs,  # Maintain the original CRS
                        transform=dataset.transform  # Maintain the original transform
                    ) as dst:
                        dst.write(self.processed_image, 1)

                    print(f"Processed image saved to {save_path}")
            except Exception as e:
                print(f"Error saving the processed image: {e}")
        else:
            print("No processed image to save.")

# Create and run the GUI
if __name__ == "__main__":
    root = Tk()
    app = GeoTIFFProcessor(root)
    root.mainloop()
