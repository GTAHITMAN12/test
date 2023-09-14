
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
x=input()
def tothai(x):
    i=0
    ln=["","สิบ","ร้อย","พัน","หมื่น","เเสน","ล้าน","สิบล้าน"]
    call = {
        '1':"หนึ่ง",
        '2':"สอง",
        '3':"สาม",
        '4':"สี่",
        '5':"ห้า",
        '6':"หก",
        '7':"เจ็ด",
        '8':"เเปด",
        '9':"ก้าว"
    }
    res=[]
    temp=1
    for value in x:
            if(value in call):
                res.append(call[value])
    #print(res)
    while i < len(x) :
        if(x[i] in call):  
            i=i+1
            #print(i)
            #print(len(ln)-i-1)
            res.insert(temp,ln[len(x)-i])
            #print(res)
            temp+=2
        else:
            i=i+1
    i=0
    for i in range(len(res)):
         #print(i)
         if res[i] == 'สอง' and res[i+1] == 'สิบ':
              res[i]='ยี่'
         if res[i-1] == 'สิบ' and res[i] == 'หนึ่ง':
              res[i]='เอ็ด'
         if res[i] == 'สิบล้าน':
              res.pop(i-1)
         if res[i] == '':
              res.pop(i)
    print(res)            
    for ans in res :
         print(ans,end=" ")
    #return res
tothai(x)
        