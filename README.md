# Zotero PDF Annotation Export（自用）
## 程序介绍
这是一个将Zotero的pdf批注、高亮导出为markdown与csv的程序。采用的是笨办法，不能完全实现自动化。  
通过Python访问Zotero本地的sqlite数据库（不会执行任何写操作），通过搜索我们人为添加的特定关键词注释，找到对应的item，导出至csv之后再进一步修改。在最后的markdown文件里，保留了Color, Text, Comment, Page, Type五类元素，并给Color列的元素添加了对应颜色。  
您也可以将任意含有注释的pdf文件导入到Zotero，再用这个程序处理，实现“pdf注释导出”的功能（这其实才是我的动机）。
## 操作步骤
1. 下载zotero_annotation_export.py。
2. 修改代码里的“文件路径”部分的路径，其中sqlite位置见[Zotero官方文档](https://www.zotero.org/support/dev/client_coding/direct_sqlite_database_access)。
3. 请在Zotero里对需要导出的pdf文件里任意位置打上注释(Add Note)"outputanno"（也可在python里自定义keyword）。若多个文件都被注释，它们的批注将会被导出至同一个markdown的不同表格里。
4. **关闭Zotero**，否则我们无权访问sqlite。运行zotero_annotation_output.py，并到对应路径查看结果。会生成两个csv（sqlite导出后、二次修改后）和一个markdown文件。
5. **打开Zotero，手动删除此前注释的keyword**
## 注
技术支持by Kimi.ai
