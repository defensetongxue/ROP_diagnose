## task binary
### model: inception_v3
setting: pretrained param:default
    acc:0.947895 auc:0.958379
### model inception_v3
setting: non_pretrained param:default
    acc:0.924568 auc:0.947926
### model Vess(LadderNet)+Class(inception_v3)
setting: vess pretrained class pretrained
    Test: acc:0.877310 auc:0.904614