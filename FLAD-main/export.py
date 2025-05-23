import os
import torch
from efficientnet_pytorch import EfficientNet

def export(model_path, export_path):
    model = EfficientNet.from_name('efficientnet-b0', num_classes=4)
    model.set_swish(memory_efficient=False)
    try:
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    except RuntimeError: # is nn.DataParallel
        state_dict = {
            k.replace('module.', ''):v for k, v in torch.load(model_path).items()
        }
        model.load_state_dict(state_dict)
    model.eval()

    dummy_input = torch.randn(1, 3, 400, 400)
    torch.onnx.export(
        model, dummy_input, 
        export_path, 
        input_names=['input'], output_names=['output'],
        verbose=True
    )

    os.system(f'python -m onnxsim "{export_path}" "{export_path}"')

export('save/model_fin.pth', 'onnx/flad.onnx')
