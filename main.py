# import io
import os.path

import streamlit as st
import streamlit.components.v1 as components
#from streamlit_javascript import st_javascript
from PIL import Image
import cns
import ych
import lxml.html
import codecs

# import tkinter as tk
# from tkinter import filedialog

# c_image = st.sidebar.selectbox(
#    'Select content',
#    ('b.png', 'input.png')
# )
sv_clrs = 0
st.markdown("<h1 style='text-align: center; color: black;'>Сервис для комбинированной стилизации изображений</h1>",
            unsafe_allow_html=True)


# def load_image():
#     image = Image.open(c_img)
#     st.image(image, width=300)
out_img = "output/ref1.png"
image_size = 320
epochs = 1
batch_size = 4
dataset = 'val2017'
save_model_dir = 'models'
content_weight = 1e5
style_weight = 1e10
lr = 1e-3
log_interval = 1
style_size = 256
flag = 0
c_image = None
s_images = None
choose = None

with st.sidebar:
    st.title('Обучить модель')
    t_image = st.file_uploader("Загрузите стиль для обучения", type=["png", "jpg", "jpeg"])
    st.title('Исходное изображение')

    c_option = st.selectbox('Загрузите изображение или сделайте фото', ('Upload_image', 'Take_a_photo'))
    # blabla = st.button("Добавить в селектбокс")
    # if blabla:
    #    c_option.append('chota')
    if c_option == 'Upload_image':
        upload_c_image = st.file_uploader("Загрузите исходное изображение", type=["png", "jpg", "jpeg"])
        if upload_c_image:
            c_image = upload_c_image
    elif c_option == 'Take_a_photo':
        take_a_photo = st.camera_input("Сделайте фото")
        if take_a_photo:
            c_image = take_a_photo

# accept_multiple_files=True)

    if c_image is not None:
        # print(type(c_image))
        # if len(c_image) != 0:
        # Посмотреть подробности
        # st.write(type(c_image))
        # file_details = {"Название файла": c_image.name,
        #                "Тип файла": c_image.type,
        #                "Размер файла": c_image.size}
        # st.write(file_details)
        # if len(c_image) != 0:
        with open(os.path.join('input', c_image.name), "wb") as f:
            f.write(c_image.getbuffer())
        # st.success("Файл сохранён")
        c_img = os.path.join("input", c_image.name)
        st.write("### Исходное изображение:")
        st.write("Название изображения: ", c_image.name)
        image = Image.open(c_img)
        st.image(image, width=300)


# save_content_path = 'C:/CNS/input/'
# completeName = os.path.join(save_content_path, c_image.name)
# img.save(completeName)


# with st.sidebar:
#     s_image = st.file_uploader("Upload style image", type=["png", "jpg", "jpeg"], accept_multiple_files=1)
#
# save_styles_path = 'C:/CNS/input/'
# completeName = os.path.join(save_styles_path, s_image.name)
# img = Image.open(s_image)
# img.save(completeName)

# s_image = st.sidebar.selectbox(
#    'Select style',
#    ('more.jpg', 'volna.jpg')
# )

# root = tk.Tk()
# root.withdraw()
# root.wm_attributes('-topmost', 1)
# with st.sidebar:
#     st.title('Стиль')
#     st.write('Пожалуйста выберите папку с вашими стилями:')
#     clicked = st.button('Выбрать папку')
#     if clicked:
#         dirname = st.text_input('Выберите папку:', filedialog.askdirectory(master=root))
#         if dirname is not None:
#             # Посмотреть подробности
#             st.write(type(dirname))

    st.title('Стиль')
    s_option = st.selectbox('Загрузите свои стили или выберите готовый', ('Upload_styles', 'Choose_model'))
    if s_option == 'Upload_styles':
        upload_s_image = st.file_uploader("Загрузите стилевые изображения", type=["png", "jpg", "jpeg"],
                                          accept_multiple_files=True)
        if upload_s_image:
            s_images = upload_s_image
    elif s_option == 'Choose_model':
        choose_model = st.selectbox("Выберите модель",
                                    ('epoch_10_Fri_Jan_21_15_44_53_2022_100000.0_100000.0',
                                     'ahr0cdovl3d3dy5saxzlc2n1.jpg_epoch_1_100000.0_10000000000.0',
                                     'Artist Creates Magical And Whimsical Illustrations.jpg_epoch_1_100000.0_'
                                     '10000000000.0',
                                     'epoch_1__100000.0_10000000000.0',
                                     'Монтажная област124ь 1.jpg_epoch_1_100000.0_10000000000.0', 'lion'))
        if choose_model:
            choose = choose_model

    if s_images is not None:
        if len(s_images) != 0:
            st.write("### Изображения стилей:")
            # while os.path.exists("style" + str(i)) is True:
            c = 1
            flag = 0
            dirname = "style{}"
            while os.path.exists(dirname.format(c)):
                if len(os.listdir(dirname.format(c))) == 0:
                    # dirname = dirname.format(c)
                    flag = 1
                    break
                else:
                    # dirname = dirname.format(c)
                    c += 1
            # dirname = dirname.format(c)
            if flag == 0:
                os.mkdir(dirname.format(c))
            s_img = dirname.format(c)

            # st.write(len(s_image))
            for s_image in s_images:
                # bytes_data = s_image.read()
                image = Image.open(s_image)
                st.write("Название стиля: ", s_image.name)
                st.image(image, width=300)

                with open(os.path.join(dirname.format(c), s_image.name), "wb") as f:
                    f.write(s_image.getbuffer())
                # st.success("Файл сохранён")
            # st.write(type(i))
            # file_details = {"Название файла": i.name,
            #                 "Тип файла": i.type,
            #                 "Размер файла": i.size}
            # st.write(file_details)
            # with open(os.path.join('style', i.name), "wb") as f:
            #     f.write(i.getbuffer())
            # st.success("Файл сохранён")
            # i += 1
            # Посмотреть подробности

if c_image and choose is not None:
    st.write('Нажмите, чтобы применить обученный стиль к исходному изображению')
    m_btn = st.button("Применить модель")
    model = os.path.join('models', choose + '.model')
    # st.write(model)
    if m_btn:
        ych.stylize(c_img, model, out_img)
        col1, col2 = st.columns(2)
        with col1:
            st.write("Исходное изображение:")
            image = Image.open(c_img)
            st.image(image, use_column_width=True)
        with col2:
            st.write("Стилизованное изображение:")
            image = Image.open(out_img)
            st.image(image, use_column_width=True)

if s_images is None:
    if c_image is None:
        if t_image is not None:
            st.write('Нажмите, чтобы обучить модель новому стилю')
            t_btn = st.button("Обучить модель")
            # st.write(model)
            if t_btn:
                ych.train(image_size, epochs, batch_size, dataset, save_model_dir, content_weight, style_weight, lr,
                          log_interval, style_size, t_image)
                st.success('Модель успешно обучена')



html_share = '''
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>GTCoding</title>
<link rel="stylesheet" href="style.css" />
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/css/all.min.css"
/>
<div class="share-btn-container">
    <a href="#" class="pinterest-btn">
      <i class="fab fa-pinterest"></i>
    </a>
</div>

<div class="content">
  <img
    class="pinterest-img"
    src="https://images.unsplash.com/photo-1535223289827-42f1e9919769?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
    alt=""
  />
</div>
<script language="javascript">
    const pinterestBtn = document.querySelector(".pinterest-btn");
    
    function init() {
      const pinterestImg = document.querySelector(".pinterest-img");
    
      let postUrl = encodeURI(document.location.href);
      let postTitle = encodeURI("Hi everyone, please check this out: ");
      let postImg = encodeURI(pinterestImg.src);
    
      pinterestBtn.setAttribute(
        "href",
        `https://pinterest.com/pin/create/bookmarklet/?media=${postImg}&description=${postTitle}`
      );

    } 
    init();
</script>
'''
yasharu = '''
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GTCoding</title>
    <link rel="stylesheet" href="style.css" />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/css/all.min.css"
    />
    <div class="share-btn-container">

      <a href="#" class="pinterest-btn">
        <i class="fab fa-pinterest"></i>
      </a>

    <div class="content">

      <img
        class="pinterest-img"
        src="https://images.unsplash.com/photo-1535223289827-42f1e9919769?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
        alt=""
      />
    </div>
<script type="text/javascript" src="//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-62ab30e2d4928946"></script>'''
components.html(yasharu)
if s_images and c_image is not None and t_image is None:
    iters = st.number_input('Количество итераций:', value=10)
    s_scl = st.number_input('Масштаб стиля', value=1.0)
    # st.write(type(s_blend_w))
    # st.write(s_scl)
    s_blend_w = []
    if len(s_images) > 1:
        for s_image in s_images:
            blend_slider = st.slider('Изменение влияния стиля: ' + str(s_image.name), 0, 100, 50, 5)
            s_blend_w.append(blend_slider)

    sw = st.number_input('Влияние стиля:', value=1000)
    clr_cb = st.checkbox("Сохранить цвета")
    s_btn = st.button("Стилизовать")

# st.write("### Styles Images:")
# image = Image.open(s_img)
# st.image(image, width=400)

# st.write("### Styles Images:")
# image = Image.open(c_img)
# st.image(image, width=400
    if s_btn:
        if clr_cb:
            sv_clrs = 1

        # model = 'models/epoch_10_Fri_Jan_21_15_44_53_2022_100000.0_100000.0.model'
        cns.main(c_img, s_img, out_img, sv_clrs, s_scl, s_blend_w, iters, sw)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Исходное изображение:")
            image = Image.open(c_img)
            st.image(image, use_column_width=True)
        with col2:
            st.write("Стили:")
            for s_image in s_images:
                # bytes_data = s_image.read()
                image = Image.open(s_image)
                st.image(image, use_column_width=True)
        with col3:
            st.write("Стилизованное изображение:")
            image = Image.open(out_img)
            st.image(image, use_column_width=True)
# shr_btn = st.button('Sahar')
# if shr_btn:

# components.html(html_share)
