from markitdown import MarkItDown
from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv()

hf_client = OpenAI(api_key=os.getenv("HF_KEY"), base_url="https://api-inference.huggingface.co/v1/")
ds_client = OpenAI(api_key=os.getenv("DEEPSEEK_KEY"), base_url="https://api.deepseek.com")
md = MarkItDown(llm_client=hf_client, llm_model="Qwen/Qwen2.5-1.5B-Instruct")

supported_extensions = ('.pptx', '.docx', '.pdf', '.jpg', '.jpeg', '.png')
data_dir = '/workspaces/qi_doc/data'

# 生成包含完整路径的文件列表
files_to_convert = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.lower().endswith(supported_extensions)]

# 用于存储所有转换后的内容
combined_content = ""

for file in files_to_convert:
    print(f"\nConverting {file}...")
    try:
        result = md.convert(file)
        
        # 将内容追加到合并的内容中，并使用指定格式进行分隔
        combined_content += f"=========={os.path.basename(file)}开始==========\n"
        combined_content += result.text_content
        combined_content += f"=========={os.path.basename(file)}结束==========\n\n"
        
        print(f"Successfully converted {file}")
    except Exception as e:
        print(f"Error converting {file}: {str(e)}")

print("\nAll conversions completed!")

# 构建提示词
prompt = f"""
你是一个专业的文档撰写助手，擅长学习已有文档的写作风格。以下是你需要参考的文档：

{combined_content}

现在请你仿照上述文档的写作风格，根据下面的新的要求来撰写一篇新的文档：
1. 
2. 
3. 
"""

# 将 prompt 保存为 Markdown 文件
prompt_md_file = os.path.join(data_dir, 'prompt.md')
with open(prompt_md_file, 'w') as file:
    file.write(prompt)

print(f"Prompt has been saved to {prompt_md_file}")

'''
# 调用大模型生成新文档
response = ds_client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个专业的文档撰写助手，擅长根据已有的文档风格和新的要求生成高质量的文档。"},
        {"role": "user", "content": prompt}
    ]
)

# 获取生成的文档内容
new_document_content = response.choices[0].message.content

# 保存生成的文档
new_md_file = os.path.join(data_dir, 'new_document.md')
with open(new_md_file, 'w') as file:
    file.write(new_document_content)

print(f"New document has been saved to {new_md_file}")
'''