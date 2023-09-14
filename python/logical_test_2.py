
"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
x=int(input())
def toroman(x):
    rules = (
        ("M", 1000),
        ("CM", 900),
        ("D",  500),
        ("CD", 400),
        ("C",  100),
        ("XC",  90),
        ("L",   50),
        ("XL",  40),
        ("XXX", 30),
        ("XX",  20),
        ("X",   10),
        ("IX",   9),
        ("V",    5),
        ("IV",   4),
        ("I",    1),
    )
    res=""
    for roman,value in rules:
            while x>=value:
                    x=x-value
                    res=res+roman
    return res
print(toroman(x))
        