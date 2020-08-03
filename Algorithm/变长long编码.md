[TOC]

# 变长Long编码

long数据类型在Java中占用8个字节，如果业务场景中，大量使用long，比如long的数组，在Hadoop和Neo4j中，都有大量使用long的场景，因此都提供了压缩型的long类型。

## 1. 核心思想

1. 用一个字节的空间表示long类型数据的字节长度，只存储8个字节中，从低位到高位，所有包含1的字节；

2. 由于负数的补码编码规则，值越小，1越多，所以对于负数，将其取反，那么高位的数字就由1编程了0，进而也就可以压缩了。

## 2. 实现

```java
public static void writeVLong(DataOutput stream, long i) throws IOException {  
// 如果在一个字节可以表示的范围内 直接返回
 if (i >= -112 && i <= 127) {  
     stream.writeByte((byte)i);  
     return;  
   }  
    //把负数变成正数
   int len = -112;  
   if (i < 0) {  
     i ^= -1L; // take one's complement'  
     len = -120;  
   }  

  //判断正数有几个位数 通过右移实现  
   long tmp = i;  
   while (tmp != 0) {  
     tmp = tmp >> 8;  
     len--;  
   }  

   // 写入第一个字节 该字节标识 这个数十正数还是负数 以及接下来有几个字节属于这个数
   stream.writeByte((byte)len);  

   // 判断需要几个字节表示该数  
   len = (len < -120) ? -(len + 120) : -(len + 112);  

//以每八位一组截取 成一个字节
  
   for (int idx = len; idx != 0; idx--) {  
     int shiftbits = (idx - 1) * 8;  
     long mask = 0xFFL << shiftbits;  
     stream.writeByte((byte)((i & mask) >> shiftbits));  
   }  
 }  
```

```java
public static long readVLong(byte[] bytes, int start) throws IOException {  
    int len = bytes[start];  
    if (len >= -112) {  
      return len;
    }  
    boolean isNegative = (len < -120);
    len = isNegative ? -(len + 120) : -(len + 112);
    if (start+1+len>bytes.length)
      throw new IOException(  
                            "Not enough number of bytes for a zero-compressed integer");  
    long i = 0;  
    for (int idx = 0; idx < len; idx++) {
      i = i << 8;  
      i = i | (bytes[start+1+idx] & 0xFF);  
    }  
    return (isNegative ? (i ^ -1L) : i);
  }
```
