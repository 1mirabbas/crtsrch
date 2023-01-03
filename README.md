# crtsrch
```
 Certificate Search
```

## Installation Steps

1. Clone crtsrch from git:
```
git clone https://github.com/1mirabbas/crtsrch.git
```
2. Change the directory:
```
cd crtsrch
```

3. Install the requirements:

```
pip3 install -r requirements.txt
```
4. Enjoy the Tool.



## Usage

Short Form    | Description
------------- |----------------------------------------------------------
-d            | Domain in which you want to find subdomains.
-o            | Output file name in which you need to save the results.



## Examples

* To list help about the tool:
```
python3 crtsrch.py -h
```
* To find subdomains
```
python3 crtsrch.py -d example.com
```

* To save the results in (output.txt) file:
```
python3 crtsrch.py -d example.com -o output.txt
```

