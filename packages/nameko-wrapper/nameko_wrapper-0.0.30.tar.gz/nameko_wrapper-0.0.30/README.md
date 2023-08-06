# Nameko Wrapper

`nameko-wrapper`包主要包含了一些编写`nameko`微服务所需要的常用工具，主要包括`nameko方法优化`，`elasticsearch优化`，`统一异常处理`以及一些其他工具。



## Nameko方法优化

- rpc异常处理优化

  `nameko_wrapper.rpc.rpc`对`nameko rpc`进行异常处理和响应优化，处理合理微服务产生的异常和统一响应内容格式。

- rpc响应优化

  `nameko_wrapper.response`为微服务响应提供统一的响应

- nameko异常统一

  `nameko_wrapper.exception`为编写微服务应用提供统一的异常类，可以方便用户自己定义处理异常；

- 常见依赖注入添加

  `nameko_wrapper.dependency_provider`提供常见的`nameko 依赖注入`，比如Elasticsearch依赖注入



## ElasticSearch优化

- 文档搜索优化

- 提供文档初始化函数

  `nameko_wrapper.elasticsearch.documents.init_document_index`

- 提供更简洁的搜索方式

- 扩展官方的文档类，提供`唯一约束`和诸多便捷查询方法

  `nameko_wrapper.elasticsearch.documents.ExtendDocument`



## 其它工具

- `nameko`配置读取方法

  `nameko_wrapper.config`

- dict访问转属性访问的方法

  `nameko_wrapper.utils.converts.dict2obj`