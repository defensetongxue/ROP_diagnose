import torch.optim as optim
import torch.nn as nn
from torch.autograd import Variable
import torch
from sklearn.metrics import roc_auc_score


class train_process():
    def __init__(self, epoch, loss_func=nn.CrossEntropyLoss):
        super(train_process, self).__init__()
        self.epoch = epoch
        self.loss_func = loss_func

    def train(self, model, train_loader, test_loader, train_len, test_len,
              optimizer=None, logging=False, save_model=False, model_name="None"):
        print("begin_trainning process")
        for epoch in range(self.epoch):
            model.train()
            train_loss = 0
            pred_train = []
            label_train = []
            for batch_x, batch_y in train_loader:
                batch_x, batch_y = (batch_x).cuda(), (batch_y).cuda()
                optimizer = optim.Adam(model.parameters(), lr=0.001)
                logits, aux = model(batch_x)
                loss = self.loss_func(logits, batch_y) + \
                    self.loss_func(aux, batch_y)
                pred = torch.max(logits, 1)[1]
                pred_train.append(pred)
                label_train.append(batch_y)
                train_loss += loss.data.item()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            pred_train = torch.cat(pred_train, dim=0)
            label_train = torch.cat(label_train, dim=0)
            mean_loss_train = train_loss/train_len
            mean_accu_train = (pred_train == label_train).sum()/train_len
            auc_train = roc_auc_score(pred_train.cpu(), label_train.cpu())

            # evaluation

            model.eval()
            with torch.no_grad():
                eval_loss = 0
                pred_val = []
                label_val = []
                for batch_x, batch_y in test_loader:
                    batch_x, batch_y = batch_x.cuda(), batch_y.cuda()
                    out = model(batch_x)
                    loss = self.loss_func(out.cpu(), batch_y.cpu())
                    eval_loss += loss.data.item()
                    pred = torch.max(out, 1)[1]
                    pred_val.append(pred)
                    label_val.append(batch_y)

                pred_val = torch.cat(pred_val, dim=0).cpu()
                label_val = torch.cat(label_val, dim=0).cpu()
                mean_loss_val = eval_loss/test_len
                mean_accu_val = (pred_val == label_val).sum()/test_len
                auc_val = roc_auc_score(pred_val, label_val)
                if logging:
                    print("Epoch {} Train: loss:{:.6f}, Acc:{:.6f}, Auc:{:.6f}|".format(
                        epoch, mean_loss_train, mean_accu_train, auc_train) +
                        " Val: loss:{:.6f}, Acc:{:.6f}, Auc:{:.6f}".format(
                        mean_loss_val, mean_accu_val, auc_val))

            if save_model:
                name = "{}.pkl".format(model_name)
                torch.save(model, './save_models/'+name)
