import shutil, os
import torch
from torchvision import datasets, transforms

def generate_test_data(PATH="../autodl-tmp/",TEST_DATA=100,clear=True):
    '''
    find the original data in "PATH/data" and generate test data in "PATH/test"
    '''
    
    pos_cnt=0
    neg_cnt=0
    def push_image(target_dic,file_name,label):
        target_path=os.path.join(target_dic,label)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        shutil.copy(file_name,target_path)
    def get_label(file_name:str):
        if file_name.lstrip().startswith("ROP"):
            # pos_cnt=pos_cnt+1
            return "ROP"
        else:
            # neg_cnt=neg_cnt+1
            return "NO"

    if clear:
        os.system("rm -rf {}".format(os.path.join(PATH,'test/*')))
    data_cnt=0
    test_dic=os.path.join(PATH,"test")
    for person_file in os.listdir(os.path.join(PATH,'data')):
        eye_file_name=os.path.join(PATH,'data',person_file)
        if not os.path.isdir(eye_file_name):
            continue
        for eye_file in os.listdir(eye_file_name):
            file_dic=os.path.join(PATH,'data',person_file,eye_file)
            if not os.path.isdir(file_dic):
                continue
            for file in os.listdir(file_dic):
                if not file.endswith(".jpg"):
                    print(file)
                    raise
                data_cnt+=1
                if data_cnt>TEST_DATA:
                    return pos_cnt,neg_cnt
                label=get_label(file)
                if label=="ROP":
                    pos_cnt=pos_cnt+1
                else:
                    neg_cnt=neg_cnt+1
                push_image(test_dic,os.path.join(file_dic,file),label)
    return pos_cnt,neg_cnt


def generate_dataloader(PATH="../autodl-tmp",train_proportion=0.6,batch_size=2,shuffle=True):
    '''
    generate train and test data in "pytorch.dataloader" format.
    '''
    # test_proportion=1-train_proportion

    data_transfrom = transforms.Compose([  # 图片读取样式
        transforms.Resize((299,299)),     
        transforms.ToTensor(),             # 向量化,向量化时 每个点的像素值会除以255,整个向量中的元素值都在0-1之间      
    ])
    
    full_dataset = datasets.ImageFolder(os.path.join(PATH,"test"), transform=data_transfrom)  # 指明读取的文件夹和读取方式,注意指明的是到文件夹的路径,不是到图片的路径
    
    data_size=len(full_dataset)
    train_size=int(data_size*train_proportion)
    test_size=data_size-train_size
    train_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])
    train_dataloader=torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)
    test_dataloader=torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle)
    return train_dataloader,test_dataloader,(train_dataset),(test_dataset)
                

        