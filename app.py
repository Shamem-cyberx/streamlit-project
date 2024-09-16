import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io
import rembg
import random

# Load the templates (just random filters or adjustments for now)
def apply_template(img, template_num):
    img = img.convert("RGBA")
    
    if template_num == 1:
        img = img.filter(ImageFilter.GaussianBlur(2))
    elif template_num == 2:
        img = img.filter(ImageFilter.CONTOUR)
    elif template_num == 3:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
    elif template_num == 4:
        img = img.filter(ImageFilter.EMBOSS)
    elif template_num == 5:
        img = img.rotate(45)
    else:
        # For other template numbers, apply random changes
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(random.uniform(0.8, 1.5))

    return img

# Function to remove the background using rembg
def remove_background(img):
    # Convert PIL image to byte data
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Remove the background using rembg
    output = rembg.remove(img_byte_arr)
    img_bg_removed = Image.open(io.BytesIO(output)).convert("RGBA")
    
    return img_bg_removed

# Streamlit app UI
st.title('Thumbnail Generator')

# File uploader for image upload
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the uploaded image
    img = Image.open(uploaded_file)
    
    # Resize to thumbnail size
    st.image(img, caption='Original Image', use_column_width=True)
    
    # Background Removal
    st.write("### Removing Background...")
    img_bg_removed = remove_background(img)
    st.image(img_bg_removed, caption="Background Removed", use_column_width=True)
    
    # Display a slider to choose one of 50 templates
    template = st.slider('Choose a template (1-50)', 1, 50, 1)
    
    # Apply the template
    st.write(f"### Applying Template {template}...")
    img_with_template = apply_template(img_bg_removed, template)
    
    # Show the image with template applied
    st.image(img_with_template, caption=f'Template {template} Applied', use_column_width=True)
    
    # Save the final thumbnail if needed
    st.download_button(
        label="Download the thumbnail",
        data=img_with_template.tobytes(),
        file_name=f'thumbnail_template_{template}.png',
        mime="image/png"
    )
