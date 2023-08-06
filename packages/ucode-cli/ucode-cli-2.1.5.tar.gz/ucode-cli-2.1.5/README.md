uCode CLI tools

CLI tools to prepare problems locally and to work with uCode.vn server

# Description

## DSA problem tools

## Other question tools

## Interact with ucode.vn server

# Installation
 
## Normal installation

```bash
pip install ucode-cli --upgrade
```

## Development installation

```bash
git clone https://gitlab.com/ucodevn/ucode-cli.git
cd ucode-cli
pip install --editable .
```

# Usage
## Get help
```bash
ucode --help
```

## Get help for a specific command
```bash
ucode {command} --help
```

# DSA Problem structure

## Input description

### Example 

#### Input

[//]: # (Auto)
- `integer T` - Multitest
- `integer n` `integer m` - Số lượng phần tử $n$, số lượng thao tác $m$
- `array.integer a[n]` - Các phần tử $a_i$ của mảng $a$, cách nhau bởi dấu cách
- `string s[m]` - xâu s gồm $m$ ký tự
- `double L` `double R` `[m]` - Cận trái và phải của một trong số $m$ thao tác 


#### Constraints

- `T`: [1, 100]
- `n`: (2, 1e6]
- `a[i]`: [1, 1e18)
- `L`: (1, 10000) 
- `R`: (`L`, 10000)
- Subtasks:
    - 40%: 
        - `T`: [1, 10]
        - `n`: [1, 100]
    - 30%: 
        - `n`: [100, 10000]
    - 40%: 
        - `n`: [10000, 1e6]

#### Output

- `boolean YES|NO` - Kết quả bài toán
- `integer`- Kết quả bài toán
- `double(3)`- Kết quả bài toán, với 3 chữ số sau dấu phẩy
  
#### Sample input 1

```
5 2
1 2 3 4 5
```

#### Sample output 1

```
11
```

#### Explanation

Các cặp số $(l, r)$ thỏa mãn là: $(1,1), (1,2), (1,3), (2,2), (2,3), (3,3), (3,4), (3,5), (4,4), (4,5), (5,5)$.