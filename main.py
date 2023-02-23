import torch
from CNNs.inception_v3 import build_inception3_pretrained as build_model
from dataloader import generate_test_data, generate_dataloader
from train import train_process
import torch.optim as optim
from config import argparse
from Vessel_Seg.export import vessel_seg_model
args = argparse()
print("Begin pretrain {}".format(args.pretrain))
loss_func = torch.nn.CrossEntropyLoss()
if args.GEN_DATA:
    generate_test_data(PATH=args.PATH, TEST_DATA=args.TEST_DATA)

train_loader, val_loader, test_loader, train_len, val_len, test_len, num_class = generate_dataloader(PATH=args.PATH,
                                                                                                     train_proportion=args.train_proportion,
                                                                                                     val_proportion=args.val_proportion,
                                                                                                     batch_size=args.batch_size)
model = build_model(num_classes=num_class,
                    pretrained=args.pretrain).cuda()  # todo model_setting
Vessel_Seg_model = vessel_seg_model(patch_height=args.ves_patch_height,
                                    patch_width=args.ves_patch_wideth,
                                    stride_height=args.ves_stride_height,
                                    stride_width=args.ves_stride_width)

train_processer = train_process(epoch=args.epoch, loss_func=loss_func)
optimizer = optim.Adam(model.parameters(), lr=args.lr)

train_processer.train(model=model,
                        ves_model=Vessel_Seg_model,
                      train_loader=train_loader,
                      val_loader=val_loader,
                      test_loader=test_loader,
                      train_len=train_len,
                      val_len=val_len,
                      test_len=test_len,
                      optimizer=optimizer,
                      logging=True)
print("data_size: train:{}, val:{}, test:{}".format(train_len, val_len, test_len))
