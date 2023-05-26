import argparse
import torch
import numpy as np

'''
	python main.py --cpu -> cpu에서 동작
	python main.py -> gpu에서 동작
'''
#====================================================================#

parser = argparse.ArgumentParser()
parser.add_argument('--cpu', action='store_true',help='run in cpu') 
args = parser.parse_args()

if args.cpu:
    device = torch.device('cpu')
else:
    device = torch.device('cuda')
#====================================================================#

def make_tensor():
    a = torch.tensor([[1,2],[3,2]], dtype=torch.int16)
    # float
    b = torch.tensor([2], dtype=torch.float32)
    # double & cuda (3 ways)
    c = torch.tensor([2], dtype=torch.float64, device=device)
    # cuda 3 ways
    # c = torch.tensor([2], dtype=torch.float64, device="cuda")
    # d = torch.tensor([2], dtype=torch.float64).cuda()
    # e = torch.tensor([2], dtype=torch.float64).to("cuda")

    print(a,b,c)

    # tensor shape , demension
    tensor_list = [a, b, c]

    for t in tensor_list:
        print("shape of tensor{}".format(t.shape)) 
        print("data type of tensor{}".format(t.dtype))
        print("device type of tensor{}".format(t.device))

def sumsub_tensor():
    a = torch.tensor([3,2])
    b = torch.tensor([5,3])

    print("input {}, {}".format(a,b))

    # sum 
    sum = a + b
    print("sum : {}".format(sum))

    # sub
    sub = a - b
    print("sub : {} ".format(sub))

    sum_element_a = a.sum()
    print("sum of matrix element : {}".format(sum_element_a))

# reference : https://paul-hyun.github.io/nlp-tutorial-02-01-matrix-equations/
def muldiv_tensor():
    a = torch.arange(0,9).view(3,3) 
    b = torch.arange(0,9).view(3,3) 
    # arange : start - end value -> tensor
    # view :  to make n-dimensional (3,3) -> 2d-mensional 
    print("input tensor \n{}, \n{}".format(a,b))

    # matrix multiplication AxB : AB
    c = torch.matmul(a,b)
    print("matrix multi : {}".format(c))

    # element-wise multiplication A⊙B
    d = torch.mul(a,b)
    print(d)

def reshape_tensor():
    a = torch.tensor([2,3,5,6,7,8])
    print("input tensor : \n{}".format(a))

    # view
    b = a.view(2,3)
    print("view : \n{}".format(b))

    # transpose
    bt = b.t()
    print("transpose : \n{}".format(bt))

def access_tensor(): # to approch data indexing
    a = torch.arange(1, 13).view(4,3)

    print("input tensor : \n{}".format(a))

    # first col (slicing)
    print(a[:,0])

    # first row (slicing)
    print(a[0,:])

    # [1,1]
    print(a[1,1])

def transform_numpy():
    a = torch.arange(1,13).view(4,3)
    print("input tensor : \n{}".format(a))

    a_np = a.numpy()
    print("numpy : {}".format(a_np))

    b = np.array([1,2,3])
    bt = torch.from_numpy(b)

    print(type(b))
    print(type(bt))

# 2d+2d -> 2d
def concat_tensor(): # if dim shapes aren't same it can't be concat. 
    a = torch.arange(1, 10).view(3,3)
    b = torch.arange(10,19).view(3,3)
    c = torch.arange(19, 28).view(3,3)

    abc_row = torch.cat([a,b,c], dim=0)
    abc_col = torch.cat([a,b,c], dim=1)
    print("input tensor : \n{}, \n{}, \n{}".format(a,b,c))
    print("concat_row(dim0) : \n{}".format(abc_row))
    print("concat_col(dim1) : \n{}".format(abc_col))

# 2d+2d -> 3d
def stack_tensor(): # if dim shapes aren't same it can't be concat. 
    a = torch.arange(1, 10).view(3,3)
    b = torch.arange(10,19).view(3,3)
    c = torch.arange(19, 28).view(3,3)

    abc = torch.stack([a,b,c], dim=0)
    print("input tensor : \n{}, \n{}, \n{}".format(a,b,c))
    print("stack : \n{}".format(abc))
    print(abc.shape)

def transpose_tensor():
    a = torch.arange(1,10).view(3,3)
    print("a tensor : \n {}".format(a))
    
    a_t = torch.transpose(a,0,1)
    
    print("a transposed : \n {}".format(a_t))
    
    b = torch.arange(1,25).view(4,3,2)
    
    print("b tensor : \n {}".format(b))
    
    b_t = torch.transpose(b,0,2)
    print("b transposed : \n {}".format(b_t))
    
    b_p = b.permute(2,0,1)
    print("b permute : \n {}".format(b_p))

if __name__ == "__main__":
    # make_tensor()
    # sumsub_tensor()
    # muldiv_tensor()
    # reshape_tensor()
    # access_tensor()
    # transform_numpy()
    # concat_tensor()
    # stack_tensor()
    transpose_tensor()
