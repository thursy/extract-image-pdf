import pandas as pd
import fitz

from utils.cosresources import *


def parsing_pdf(tempfile, filename, bucket_name, endpoint_url_public, res):
    pdf_document = fitz.open(tempfile)
    doc_text_blocks = [page.get_text("blocks") for page in pdf_document]
    doc_image_blocks = [page.get_images(full=True)for page in pdf_document]

    img_list= []
    for page_num, page_img_blocks in enumerate(doc_image_blocks):
        for blocks_num, img_blocks in enumerate(page_img_blocks):
            img_dict = {}
            img_dict['page_num'] = page_num
            img_dict['block_num'] = blocks_num
            img_dict['enum_type'] = blocks_num
            img_dict['type'] = "image"
            img_dict['img_info'] = img_blocks
            img_dict['img_index'] = img_blocks[0]
            img_dict['img_binary'] = pdf_document.extract_image(img_blocks[0])['image']

            #upload the file into cos
            pdf_name = filename.split(".")[0]
            file_obj_name = f"{pdf_name}/{pdf_name}_{page_num}_{blocks_num}_{img_dict['img_index']}.png"

            try:
                #if success then compose url
                # https://cos-img-public-2023.s3.jp-tok.cloud-object-storage.appdomain.cloud/645d738f5f15f.png
                # https://{bucket_name}.{endpoint_url_public}/{file_obj_name}
                #def upload_fileobj(bucket_name, item_name, item_bin, res):
                upload_fileobj(bucket_name, file_obj_name, img_dict['img_binary'], res)
                img_dict['img_cos_url'] = f"https://{bucket_name}.{endpoint_url_public}/{file_obj_name}"
                img_dict['img_html_url'] = f'<img src="https://{bucket_name}.{endpoint_url_public}/{file_obj_name}"></img>'
            except:
                img_dict['img_cos_url'] = None
                img_dict['img_html_url'] = None

            img_list.append(img_dict)
    
    pd_img_url = pd.DataFrame(img_list)[["page_num","enum_type","type","img_cos_url"]]
    img_bin_list = list(pd.DataFrame(img_list)["img_binary"])
    img_url_list = list(pd_img_url['img_cos_url'])

    content_list= []
    for page_num, page_text_blocks in enumerate(doc_text_blocks):
        img_only_cnt = 0
        txt_only_cnt = 0
        for blocks_num, text_blocks in enumerate(page_text_blocks):
            content_dict = {}
            content_dict['page_num'] = page_num
            content_dict['blocks_num'] = blocks_num
            content_dict['content'] = text_blocks[4]
            if text_blocks[4][:7] == '<image:':
                content_dict['type'] = "image"
                content_dict['enum_type'] = img_only_cnt
                img_only_cnt += 1
            else:
                content_dict['type'] = "text"
                content_dict['enum_type'] = txt_only_cnt
                txt_only_cnt += 1
            content_list.append(content_dict)
            
    pd_content = pd.DataFrame(content_list)

    merged_df = pd.merge(pd_content, pd_img_url, on=['page_num', 'enum_type', 'type'], how='left')
    merged_df['content_url'] = merged_df['img_cos_url'].fillna(merged_df['content'])
    st.write(merged_df)
    merged_df = merged_df[['page_num','blocks_num','content_url']]
    df_sorted = merged_df.sort_values(by=['page_num', 'blocks_num'])
    df_output = df_sorted[['content_url']]

    return df_output, img_url_list, img_bin_list
