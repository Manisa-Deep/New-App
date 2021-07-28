import streamlit as st
from streamlit_cropper import st_cropper
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp 

mp_drawing=mp.solutions.drawing_utils
mp_face_mesh=mp.solutions.face_mesh

model_face_mesh=mp_face_mesh.FaceMesh()
st.title('Welcome to Play with image operations App')

image=st.sidebar.file_uploader('Upload Image')
for_crop=image
if image is not None:
	image=Image.open(image)
	image=np.array(image)
	st.sidebar.image(image)

add_selectbox = st.sidebar.selectbox(
	'What operations you would like to perform?',
	('About', 'Add Filters', 'Image Blending Effects', 'Image Croping', 'Image Rotating', 'Face Meshing', 'Cartoon Image', 'Image Blurr')
	)
if add_selectbox=='About':
	st.header('Here we will use different operations of OpenCV')
	st.write('\n')
	st.write('In this App you will be doing operations like image filtering, image blending, image croping, image rotating and face meshing')
	st.write("""1. Add Filters: In Add filters, it adds different color to your image according to your choice out of
	               four given choices that are Red, Green, Blue and Black and White.""")
	st.write('2. Image Blending Effects: Here you can blend two images of your choice in order to give one image effect on the other image.')
	st.write('3. Image Croping: In image croping, it gives access to you to crop your image with your given choice for croping.')
	st.write('4. Image Rotating: Here you can rotate you image in anticlockwise or clockwise on any angle you want.')
	st.write("5. Face Meshing: Here the given image's face will be detected and the different parts of your face will be shown with coordinates or dots.")
	st.subheader("So I hope guys you will definitely have fun by using this App.")
	st.subheader("             SO LET'S  GET STARTED !")

if add_selectbox=='Add Filters':
	choice=st.sidebar.radio(
		"Select your filter color",
		('None','Red', 'Green', 'Blue', 'Black and White'))

	if choice=='Red':
		zeros=np.zeros((image.shape[0], image.shape[1]), np.uint8)
		b,g,r=cv2.split(image)
		Red=cv2.merge([r, zeros, zeros])
		st.image(Red)

	elif choice=='Green':
		zeros=np.zeros((image.shape[0], image.shape[1]), np.uint8)
		b,g,r=cv2.split(image)
		Green=cv2.merge([zeros, g, zeros])
		st.image(Green)

	elif choice=='Blue':
		zeros=np.zeros((image.shape[0], image.shape[1]), np.uint8)
		b,g,r=cv2.split(image)
		Blue=cv2.merge([zeros, zeros, b])
		st.image(Blue)
	
	if choice=='Black and White':
		image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		st.image(image)

elif add_selectbox=='Face Meshing':
	results=model_face_mesh.process(image)

	for face_landmarks in results.multi_face_landmarks:
		mp_drawing.draw_landmarks(image, face_landmarks)
	st.image(image)
elif add_selectbox=='Image Blending Effects':
	image2=st.sidebar.file_uploader('Upload another image to blend the above image')
	if image2 is not None:
		image2=Image.open(image2)
		image2=np.array(image2)
		st.sidebar.image(image2)
		image2=cv2.resize(image2, (image.shape[1], image.shape[0]))
		blended_img=cv2.addWeighted(image, 0.7, image2, 0.3, gamma=1.5)
		st.image(blended_img)
elif add_selectbox=='Image Croping':
	realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
	aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
	aspect_dict = {"1:1": (1,1),"16:9": (16,9),"4:3": (4,3),"2:3": (2,3),"Free": None}
	aspect_ratio = aspect_dict[aspect_choice]
	if for_crop:
		image2=Image.open(for_crop)
	if not realtime_update:
		st.write("Double click to save crop")
	cropped_img = st_cropper(image2, realtime_update=realtime_update, aspect_ratio=aspect_ratio)
	st.write("Preview")
	_ = cropped_img.thumbnail((700,700))
	st.image(cropped_img)
elif add_selectbox=='Image Rotating':
	flipV=cv2.flip(image, 0)
	flipH=cv2.flip(image, 1)
	flipB=cv2.flip(image, -1)
	Fchoice=st.sidebar.radio(
		"choose flip options:",
		('None','Flip Vertically','Flip Horizontally','Flip Both'))
	if Fchoice=='None':
		st.image(image)
	if Fchoice=='Flip Vertically':
		st.image(flipV)
	elif Fchoice=='Flip Horizontally':
		st.image(flipH)
	elif Fchoice=='Flip Both':
		st.image(flipB)
elif add_selectbox=='Cartoon Image':
	gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray=cv2.medianBlur(gray, 5)
	edges=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
	color=cv2.bilateralFilter(image, 9, 250 , 250)
	cartoon=cv2.bitwise_and(color, color, mask=edges)
	st.image(cartoon)
elif add_selectbox=='Image Blurr':
	blur=cv2.medianBlur(image,5)
	st.image(blur)