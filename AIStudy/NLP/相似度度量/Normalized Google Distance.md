[TOC]

# Normalized Google Distance

归一化Google距离，Google距离是一种度量语义相似度的方法，它通过搜索引擎返回结果的数量的相似性来评估关键词的相似性。

$$
NGD(x,y) = \frac{max\{logf(x),logf(y)\} - logf(x,y)}{logN - min\{ logf(x),logf(y) \}}
$$

参数说明：
f(x)：搜索x命中的数量
f(y)：搜索y命中的数量
f(x,y)：同时搜索x,y命中的数量

N是所有页面的数量 乘以 每页中词条的数量。

如果NGD接近于0，那么x,y相似度很好；$NGD \geq 1$，那么说明两者很不相同。
