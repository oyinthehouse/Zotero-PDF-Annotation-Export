# Zotero PDF Annotation Export（自用）
## 程序介绍
- 这是一个将Zotero的pdf批注、高亮导出为Markdown与CSV的程序。采用的是笨办法，不能完全实现自动化。  
- 程序将访问Zotero本地的SQLite数据库（不会执行任何写操作），搜索我们人为添加的特定关键词注释，找到对应的item，导出至CSV，并进一步修改。在最后的Markdown文件里，保留了Color, Text, Comment, Page, Type五类元素，并给Color列的元素添加了对应颜色。并且，注释按照页面位置顺序升序排列。
- 您也可以将任意含有注释的pdf文件导入到Zotero，再用这个程序处理，实现“pdf注释导出”的功能（这其实才是我的动机）。
- 示例见example文件夹。我的版本是Zotero 6，操作系统是Windows 11。
## 操作步骤
1. 下载zotero_annotation_export.py。
2. 修改代码里的“文件路径”部分的路径，其中SQLite位置见[Zotero官方文档](https://www.zotero.org/support/dev/client_coding/direct_sqlite_database_access)。
3. 请在Zotero里对需要导出的pdf文件里任意位置打上注释(Add Note)"outputanno"（也可在程序里自定义keyword）。若多个文件都被注释，它们的批注将会被导出至同一个Markdown的不同表格里。
4. **关闭Zotero**，否则我们无权访问SQLite。运行zotero_annotation_export.py，并到对应路径查看结果。会生成两个CSV（SQLite导出后、二次修改后）和一个Markdown文件。
5. **记得在Zotero删除此前注释的keyword**，否则会把对应的pdf带到下次导出。
## 注
- 技术支持by Kimi.ai
- 我不太（懂）用GitHub和编程，所以如果您想优化程序的话，可以自行修改并发布，不需要pull request到这个仓库里。谢谢！
