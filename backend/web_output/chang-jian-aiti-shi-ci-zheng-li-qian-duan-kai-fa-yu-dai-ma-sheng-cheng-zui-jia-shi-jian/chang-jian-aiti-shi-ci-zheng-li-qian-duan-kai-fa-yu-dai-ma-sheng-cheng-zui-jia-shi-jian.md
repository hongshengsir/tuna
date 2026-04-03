# 常见AI提示词整理——前端开发与代码生成最佳实践

**作者**: 未知作者
**发布日期**: 未知
**下载时间**: 2026-03-29 15:22:53
**媒体资源数量**: 4

---



[老猫-Bond](/developer/user/3560095)

## 常见AI提示词整理——前端开发与代码生成最佳实践

关注作者

[*腾讯云*](/?from=20060&from_column=20060)[*开发者社区*](/developer)

[文档](/document/product?from=20702&from_column=20702)[建议反馈](/voc/?from=20703&from_column=20703)[控制台](https://console.cloud.tencent.com?from=20063&from_column=20063)

登录/注册

[首页](/developer)

学习

活动

专区

圈层

工具

[MCP广场![](image_001.png)](/developer/mcp)

文章/答案/技术大牛搜索

搜索关闭

发布

老猫-Bond

[社区首页](/developer) >[专栏](/developer/column) >常见AI提示词整理——前端开发与代码生成最佳实践

# 常见AI提示词整理——前端开发与代码生成最佳实践

![作者头像](image_002.jpg)

老猫-Bond

关注

发布于 2026-03-10 17:48:07

发布于 2026-03-10 17:48:07

7790

举报

文章被收录于专栏：[前端大全](/developer/column/101457)前端大全

AI提示词是与AI工具进行有效沟通的关键，合适的提示词可以显著提升代码生成质量和开发效率。

### 介绍

  随着AI编程助手的普及，提示词工程（Prompt Engineering）已成为现代开发者的重要技能。在前端开发中，合适的AI提示词可以帮助我们快速生成高质量的代码、解决复杂的技术问题、进行代码审查和性能优化。本文将系统整理前端开发中常用的AI提示词，按功能场景分类，为开发者提供实用的参考指南。

### 代码生成类提示词

#### React组件生成

代码语言：javascript

复制

```
# 生成React函数组件

## 基础组件生成
~~~
Create a React functional component that [describe functionality].
The component should use TypeScript and follow React best practices.
Include proper TypeScript interfaces for props.
Add JSDoc comments for exported functions and components.
~~~

## 复杂组件生成
~~~
Create a [component name] component with the following requirements:
- Use React hooks (useState, useEffect, etc.)
- Include proper TypeScript types
- Follow accessibility guidelines (WCAG 2.1 AA)
- Support dark/light theme
- Include loading and error states
- Use modern React patterns (compound components, render props, etc.)

Component specification:
- [specific requirements]
- [styling framework] for styling
- [additional functionality]
~~~

## 自定义Hook生成
~~~
Create a custom React hook called use[HookName] that:
- Purpose: [describe what the hook does]
- Parameters: [describe input parameters]
- Return value: [describe return value]
- Side effects: [describe any side effects]
- Dependencies: [list external dependencies if any]

Include proper TypeScript typing and error handling.
Add comprehensive JSDoc documentation.
~~~
```

#### Vue组件生成

代码语言：javascript

复制

```
# Vue组件生成提示词

## Composition API组件
~~~
Create a Vue 3 component using Composition API that [functionality description].
Use TypeScript and follow Vue 3 best practices.

Component requirements:
- Props: [list required props with types]
- Emits: [list emitted events]
- Slots: [describe slots if needed]
- Exposed methods: [methods to expose]

Include proper TypeScript interfaces and generic typing where appropriate.
Use provide/inject for parent-child communication if needed.
~~~

## Vue组件优化
~~~
Refactor the following Vue component to improve performance and maintainability:
- Convert Options API to Composition API
- Optimize reactivity using ref/computed properly
- Add proper TypeScript typing
- Implement proper error handling
- Add loading states and error boundaries
- Follow Vue style guide recommendations
~~~
```

#### CSS/样式生成

代码语言：javascript

复制

```
# CSS样式生成提示词

## TailwindCSS组件
~~~
Create a responsive [component name] component using TailwindCSS.
The component should:
- Be fully responsive (mobile, tablet, desktop)
- Follow accessibility best practices
- Include dark mode support
- Use Tailwind's utility classes efficiently
- Be customizable with props/config

Style requirements:
- [specific color scheme]
- [typography requirements]
- [animation/transitions if needed]
- [layout constraints]
~~~

## 动画效果生成
~~~
Create CSS animations for [describe animation purpose].
Provide both pure CSS (using @keyframes) and TailwindCSS implementations.
Include:
- Smooth transitions
- Performance optimizations (using transform, opacity)
- Responsive behavior
- Accessibility considerations (prefers-reduced-motion)
- Cross-browser compatibility notes
~~~

## 复杂布局生成
~~~
Create a complex responsive layout using CSS Grid and Flexbox that:
- Has [number] columns on desktop, [number] on tablet, [number] on mobile
- Maintains aspect ratios for images/media
- Handles content overflow gracefully
- Supports RTL languages
- Optimizes for SEO and accessibility
~~~
```

### 代码优化类提示词

#### 性能优化

代码语言：javascript

复制

```
# 性能优化提示词

## 代码性能优化
~~~
Analyze and optimize the following code for performance:
- Identify performance bottlenecks
- Suggest React memoization strategies
- Optimize rendering with React.memo, useMemo, useCallback
- Implement code splitting and lazy loading
- Optimize bundle size
- Suggest algorithm improvements
- Identify unnecessary re-renders

Provide specific recommendations with code examples.
~~~

## 前端性能优化
~~~
Implement performance optimizations for a React application:
- Code splitting strategies
- Image optimization techniques
- Caching mechanisms
- Bundle size reduction
- Loading state optimizations
- Memory leak prevention
- Network request optimization

Provide specific implementation examples for each technique.
~~~
```

#### 代码重构

代码语言：javascript

复制

```
# 代码重构提示词

## 重构建议
~~~
Refactor the following code to improve:
- Readability and maintainability
- Performance
- Type safety (add TypeScript if missing)
- Error handling
- Testing strategy
- Separation of concerns
- Modern JavaScript/React patterns

Keep the same functionality but improve the code structure and quality.
~~~

## 从Class组件到Hook组件
~~~
Convert the following React class component to a functional component using hooks:
- Replace lifecycle methods with useEffect hooks
- Convert state management to useState/useReducer
- Handle refs appropriately
- Maintain the same functionality
- Add proper TypeScript typing
- Include proper cleanup functions
~~~
```

### 调试与问题解决

#### 错误排查

代码语言：javascript

复制

```
# 调试提示词

## 错误诊断
~~~
The following code is throwing [error message]. Please analyze the code and:
1. Identify the root cause of the error
2. Explain why this error occurs
3. Provide the corrected code
4. Explain the fix and why it works
5. Suggest similar errors to watch out for

Code:
[insert problematic code here]
~~~

## 性能问题诊断
~~~
The application is experiencing [performance issue description]. Please help diagnose and fix:
1. Identify potential causes
2. Suggest debugging tools to use
3. Provide code improvements
4. Recommend performance monitoring solutions
5. Estimate performance gains

Current symptoms:
- [list symptoms]
- [performance metrics if available]
- [user impact]
~~~
```

#### 代码审查

代码语言：javascript

复制

```
# 代码审查提示词

## 安全审查
~~~
Review the following code for security vulnerabilities:
- XSS prevention
- CSRF protection
- Input validation
- Sanitization practices
- Authentication/authorization issues
- Data exposure risks
- Third-party library security

Provide specific fixes for each vulnerability found.
~~~

## 质量审查
~~~
Perform a comprehensive code review focusing on:
- Code quality and readability
- Best practices adherence
- Potential bugs
- Performance considerations
- Maintainability
- Documentation completeness
- Test coverage suggestions

Rate each issue by severity and provide improvement suggestions.
~~~
```

### 国际化与多语言

#### I18n实现

代码语言：javascript

复制

```
# 国际化提示词

## 多语言支持
~~~
Implement internationalization (i18n) for the following React application:
- Use react-i18next or next-i18next
- Create language switcher component
- Implement RTL support where needed
- Handle pluralization
- Manage date/time formatting
- Handle number/currency formatting
- Organize translation files structure
- Implement fallback languages

Include proper TypeScript typing for translations.
~~~

## 翻译文件生成
~~~
Create translation files for [language] localization:
- Extract translatable strings from [provided code]
- Organize translations by domain/context
- Handle pluralization
- Include RTL language considerations
- Follow linguistic best practices
- Maintain consistency across translations

Provide both JSON structure and example translations.
~~~

## 日期时间国际化
~~~
Implement internationalized date and time formatting that:
- Uses user's locale automatically
- Handles different calendar systems
- Manages time zones properly
- Supports 12/24-hour formats
- Handles relative time (e.g., "2 hours ago")
- Includes proper TypeScript types

Use modern JavaScript Internationalization API.
~~~
```

### 测试相关

#### 单元测试生成

代码语言：javascript

复制

```
# 测试生成提示词

## React组件测试
~~~
Create comprehensive unit tests for the following React component using:
- Testing Library and React Testing Library
- Jest for test runner
- TypeScript support

Test requirements:
- Render with different props
- Handle user interactions
- Test async behavior
- Mock external dependencies
- Test edge cases
- Accessibility testing
- Snapshot testing if appropriate
~~~

## API测试
~~~
Create API tests for the following endpoints:
- Test successful responses
- Test error scenarios
- Validate response schemas
- Test authentication/authorization
- Handle different HTTP methods
- Test rate limiting
- Performance testing scenarios
- Include both happy path and error cases
~~~
```

#### 测试优化

代码语言：javascript

复制

```
# 测试优化提示词

## 测试重构
~~~
Refactor the following tests to improve:
- Test structure and organization
- Readability and maintainability
- Performance and speed
- Coverage and effectiveness
- Mock management
- Test data management
- Error handling in tests

Maintain test effectiveness while improving quality.
~~~
```

### 工具与配置

#### 开发工具配置

代码语言：javascript

复制

```
# 工具配置提示词

## ESLint/Prettier配置
~~~
Create ESLint and Prettier configuration for a modern React project that:
- Enforces React best practices
- Includes TypeScript support
- Follows Airbnb or similar style guide
- Includes React Hooks rules
- Enforces import ordering
- Includes testing library rules
- Optimizes for VS Code integration
- Provides auto-fix capabilities

Provide both base configuration and React-specific extensions.
~~~

## 构建工具配置
~~~
Configure Vite for a React project with the following requirements:
- TypeScript support
- CSS preprocessing (SASS/SCSS)
- Asset optimization
- Environment variables
- Proxy configuration for API
- Code splitting setup
- Production optimization
- Development server configuration
~~~
```

### 文档与注释

#### 代码文档

代码语言：javascript

复制

```
# 文档生成提示词

## JSDoc生成
~~~
Generate comprehensive JSDoc documentation for the following code:
- Function/method descriptions
- Parameter types and descriptions
- Return value documentation
- Exception/error documentation
- Example usage
- Accessibility considerations
- Performance implications
- Deprecation notices if applicable
~~~

## API文档
~~~
Create API documentation for the following REST endpoints:
- Request/response schemas
- Authentication requirements
- Error response formats
- Rate limiting information
- Example requests/responses
- Curl commands
- SDK usage examples
- Security considerations
~~~
```

### AI辅助开发工作流

#### 提示词优化策略

代码语言：javascript

复制

```
# 提示词优化策略

## 提示词结构
~~~
Effective AI prompt structure for code generation:

1. Role Definition: "Act as an experienced React/JavaScript developer"
2. Task Definition: "Create a component that..."
3. Constraints: "Use TypeScript, follow accessibility..."
4. Examples: "Similar to X, but with Y functionality"
5. Output Format: "Return code with comments and documentation"
~~~

## 上下文提供
~~~
When providing context to AI:

- Share relevant code snippets
- Explain business requirements
- Specify technical constraints
- Mention performance requirements
- Indicate design system components
- Reference existing patterns
- Clarify edge cases
- Specify testing requirements
~~~

## 反量反馈循环
~~~
Iterative improvement with AI:

1. Start with high-level requirements
2. Review initial output
3. Provide specific feedback
4. Request targeted improvements
5. Validate against requirements
6. Repeat until satisfied
~~~
```

### 常见场景专用提示词

#### 响应式设计

代码语言：javascript

复制

```
# 响应式设计提示词

## 移动优先设计
~~~
Create a mobile-first responsive component that:
- Starts with mobile layout
- Progressively enhances for larger screens
- Uses appropriate media query breakpoints
- Maintains touch-friendly interactions
- Optimizes for mobile performance
- Considers mobile-specific UX patterns
- Follows mobile accessibility guidelines
~~~
```

#### 可访问性

代码语言：javascript

复制

```
# 可访问性提示词

## WCAG合规
~~~
Create an accessible component that complies with WCAG 2.1 AA guidelines:
- Proper heading structure
- Sufficient color contrast
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- ARIA attributes where needed
- Alternative text for images
- Form accessibility
- Skip links for navigation
~~~
```

#### 安全编程

代码语言：javascript

复制

```
# 安全编程提示词

## 输入验证
~~~
Implement robust input validation for [specific input type] that:
- Validates data type and format
- Implements sanitization
- Prevents injection attacks
- Handles edge cases
- Provides user-friendly error messages
- Maintains good UX while being secure
- Includes both client and server validation
~~~
```

### 实用提示词模板

#### 通用代码生成模板

代码语言：javascript

复制

```
# 通用模板

~~~~
As an experienced [technology] developer, create [component/type] that:
PURPOSE: [what the code should accomplish]
REQUIREMENTS: [specific technical requirements]
CONSTRAINTS: [limitations or specific constraints]
TECHNOLOGY_STACK: [languages, frameworks, libraries]
PERFORMANCE: [speed, bundle size, etc. requirements]
ACCESSIBILITY: [compliance level required]
TESTING: [test coverage expectations]

Include:
- Proper TypeScript definitions if applicable
- Comprehensive error handling
- Performance optimizations
- Security best practices
- Accessibility features
- Documentation and comments
- Usage examples

Return production-ready code following industry best practices.
~~~~
```

#### 调试求助模板

代码语言：javascript

复制

```
# 调试模板

~~~~
I'm experiencing [specific problem] with the following code:
[provide code snippet]

EXPECTED_BEHAVIOR: [what should happen]
ACTUAL_BEHAVIOR: [what is happening]
ERROR_MESSAGES: [any error messages]
CONTEXT: [environment, browser, dependencies]

Please help me:
1. Identify the root cause
2. Provide a solution
3. Explain why the issue occurred
4. Suggest how to prevent similar issues
5. Recommend debugging tools/techniques for similar problems

Consider [specific constraints or requirements].
~~~~
```

#### 多语言翻译助手模板

代码语言：javascript

复制

```
# 多语言翻译助手

## 翻译助手角色
~~~~
Act as a professional translator. I will provide multiple texts separated by newlines. Translate each text into multiple languages and return the results in JSON format.

Languages to translate to:
- zh_CN: Simplified Chinese
- en_US: English
- ja_JP: Japanese
- ko_KR: Korean
- fr_FR: French
- de_DE: German
- es_ES: Spanish
- ar_SA: Arabic
- pt_BR: Portuguese (Brazil)
- ru_RU: Russian
- it_IT: Italian
- th_TH: Thai

Input format:
[Line 1 - text to translate]
[Line 2 - another text to translate]
[Line 3 - more text to translate]

Output format:
~~~
[
  { "lang": "zh_CN", "name": "中文", "text": "[translated text for line 1]" },
  { "lang": "en_US", "name": "英文", "text": "[translated text for line 1]" },
  { "lang": "ja_JP", "name": "日文", "text": "[translated text for line 1]" },
  { "lang": "ko_KR", "name": "韩文", "text": "[translated text for line 1]" },
  { "lang": "fr_FR", "name": "法文", "text": "[translated text for line 1]" },
  { "lang": "de_DE", "name": "德文", "text": "[translated text for line 1]" },
  { "lang": "es_ES", "name": "西班牙文", "text": "[translated text for line 1]" },
  { "lang": "ar_SA", "name": "阿拉伯文", "text": "[translated text for line 1]" },
  { "lang": "pt_BR", "name": "葡萄牙文", "text": "[translated text for line 1]" },
  { "lang": "ru_RU", "name": "俄文", "text": "[translated text for line 1]" },
  { "lang": "it_IT", "name": "意大利文", "text": "[translated text for line 1]" },
  { "lang": "th_TH", "name": "泰文", "text": "[translated text for line 1]" }
]
~~~

[Continue with translations for each input line...]

Example input:
Data Table Configuration
User Profile Management
Real-time Analytics Dashboard

Example output:
~~~
[
  { "lang": "zh_CN", "name": "中文", "text": "数据表配置" },
  { "lang": "en_US", "name": "英文", "text": "Data Table Configuration" },
  { "lang": "ja_JP", "name": "日文", "text": "データテーブル構成" },
  { "lang": "ko_KR", "name": "韩文", "text": "데이터 테이블 구성" },
  { "lang": "fr_FR", "name": "法文", "text": "Configuration du tableau de données" },
  { "lang": "de_DE", "name": "德文", "text": "Datentabellenkonfiguration" },
  { "lang": "es_ES", "name": "西班牙文", "text": "Configuración de tabla de datos" },
  { "lang": "ar_SA", "name": "阿拉伯文", "text": "تكوين جدول البيانات" },
  { "lang": "pt_BR", "name": "葡萄牙文", "text": "Configuração da tabela de dados" },
  { "lang": "ru_RU", "name": "俄文", "text": "Конфигурация таблицы данных" },
  { "lang": "it_IT", "name": "意大利文", "text": "Configurazione tabella dati" },
  { "lang": "th_TH", "name": "泰文", "text": "การกำหนดค่าตารางข้อมูล" }
]
~~~

Maintain accurate terminology and cultural appropriateness in each language.
~~~~
```

有效的AI提示词应该具体、清晰且包含足够的上下文信息。通过使用结构化的提示词模板，可以获得更准确、更符合需求的AI输出。

### 总结

  AI提示词是现代前端开发的重要工具，掌握有效的提示词技巧可以显著提升开发效率和代码质量。关键要点包括：

1. **明确目标**：清楚描述需要生成的代码功能和特性
2. **提供上下文**：包含技术栈、约束条件、性能要求等信息
3. **结构化组织**：使用清晰的结构化格式提高AI理解能力
4. **迭代优化**：根据AI输出进行调整和优化
5. **质量检查**：始终审查AI生成的代码确保质量和安全性

  随着AI技术的不断发展，提示词工程将成为前端开发者的核心技能之一。通过不断练习和优化提示词策略，开发者可以更有效地利用AI工具提升工作效率。

本文参与 [腾讯云自媒体同步曝光计划](/developer/support-plan)，分享自作者个人站点/博客。

原始发表：2025-11-29，如有侵权请联系 [cloudcommunity@tencent.com](mailto:cloudcommunity@tencent.com) 删除

前往查看

[优化](/developer/tag/17554)

[最佳实践](/developer/tag/17607)

[text](/developer/tag/16461)

[测试](/developer/tag/17205)

[配置](/developer/tag/17393)

本文分享自 作者个人站点/博客 前往查看

如有侵权，请联系 [cloudcommunity@tencent.com](mailto:cloudcommunity@tencent.com) 删除。

本文参与 [腾讯云自媒体同步曝光计划](/developer/support-plan)  ，欢迎热爱写作的你一起参与！

[优化](/developer/tag/17554)

[最佳实践](/developer/tag/17607)

[text](/developer/tag/16461)

[测试](/developer/tag/17205)

[配置](/developer/tag/17393)

评论

登录后参与评论

0 条评论

热度

最新

登录 后参与评论

推荐阅读

目录

- 介绍

- 代码生成类提示词
  - React组件生成
  - Vue组件生成
  - CSS/样式生成

- 代码优化类提示词
  - 性能优化
  - 代码重构

- 调试与问题解决
  - 错误排查
  - 代码审查

- 国际化与多语言
  - I18n实现

- 测试相关
  - 单元测试生成
  - 测试优化

- 工具与配置
  - 开发工具配置

- 文档与注释
  - 代码文档

- AI辅助开发工作流
  - 提示词优化策略

- 常见场景专用提示词
  - 响应式设计
  - 可访问性
  - 安全编程

- 实用提示词模板
  - 通用代码生成模板
  - 调试求助模板
  - 多语言翻译助手模板

- 总结

领券

- ### 社区

  - [技术文章](/developer/column)
  - [技术问答](/developer/ask)
  - [技术沙龙](/developer/salon)
  - [技术视频](/developer/video)
  - [学习中心](/developer/learning)
  - [技术百科](/developer/techpedia)
  - [技术专区](/developer/zone/list)
- ### 活动

  - [自媒体同步曝光计划](/developer/support-plan)
  - [邀请作者入驻](/developer/support-plan-invitation)
  - [自荐上首页](/developer/article/1535830)
  - [技术竞赛](/developer/competition)
- ### 圈层

  - [腾讯云最具价值专家](/tvp)
  - [腾讯云架构师技术同盟](/developer/program/tm)
  - [腾讯云创作之星](/developer/program/tci)
  - [腾讯云TDP](/developer/program/tdp)
- ### 关于

  - [社区规范](/developer/article/1006434)
  - [免责声明](/developer/article/1006435)
  - [联系我们](mailto:cloudcommunity@tencent.com)
  - [友情链接](/developer/friendlink)
  - [MCP广场开源版权声明](/developer/article/2537547)

### 腾讯云开发者

![扫码关注腾讯云开发者](image_003.png)

扫码关注腾讯云开发者

领取腾讯云代金券

### 热门产品

- [域名注册](/product/domain?from=20064&from_column=20064)
- [云服务器](/product/cvm?from=20064&from_column=20064)
- [区块链服务](/product/tbaas?from=20064&from_column=20064)
- [消息队列](/product/message-queue-catalog?from=20064&from_column=20064)
- [网络加速](/product/ecdn?from=20064&from_column=20064)
- [云数据库](/product/tencentdb-catalog?from=20064&from_column=20064)
- [域名解析](/product/dns?from=20064&from_column=20064)
- [云存储](/product/cos?from=20064&from_column=20064)
- [视频直播](/product/css?from=20064&from_column=20064)

### 热门推荐

- [人脸识别](/product/facerecognition?from=20064&from_column=20064)
- [腾讯会议](/product/tm?from=20064&from_column=20064)
- [企业云](/act/pro/enterprise2022?from=20064&from_column=20064)
- [CDN加速](/product/cdn?from=20064&from_column=20064)
- [视频通话](/product/trtc?from=20064&from_column=20064)
- [图像分析](/product/imagerecognition?from=20064&from_column=20064)
- [MySQL 数据库](/product/cdb?from=20064&from_column=20064)
- [SSL 证书](/product/ssl?from=20064&from_column=20064)
- [语音识别](/product/asr?from=20064&from_column=20064)

### 更多推荐

- [数据安全](/solution/data_protection?from=20064&from_column=20064)
- [负载均衡](/product/clb?from=20064&from_column=20064)
- [短信](/product/sms?from=20064&from_column=20064)
- [文字识别](/product/ocr?from=20064&from_column=20064)
- [云点播](/product/vod?from=20064&from_column=20064)
- [大数据](/product/bigdata-class?from=20064&from_column=20064)
- [小程序开发](/solution/la?from=20064&from_column=20064)
- [网站监控](/product/tcop?from=20064&from_column=20064)
- [数据迁移](/product/cdm?from=20064&from_column=20064)

Copyright © 2013 - 2026 Tencent Cloud. All Rights Reserved. 腾讯云 版权所有

[深圳市腾讯计算机系统有限公司](https://qcloudimg.tencent-cloud.cn/raw/986376a919726e0c35e96b311f54184d.jpg) ICP备案/许可证号：[粤B2-20090059](https://beian.miit.gov.cn/#/Integrated/index)![](image_004.png)[粤公网安备44030502008569号](https://beian.mps.gov.cn/#/query/webSearch?code=44030502008569)

[腾讯云计算（北京）有限责任公司](https://qcloudimg.tencent-cloud.cn/raw/a2390663ee4a95ceeead8fdc34d4b207.jpg) 京ICP证150476号 |  [京ICP备11018762号](https://beian.miit.gov.cn/#/Integrated/index)

[问题归档](/developer/ask/archives.html)[专栏文章](/developer/column/archives.html)[快讯文章归档](/developer/news/archives.html)[关键词归档](/developer/information/all.html)[开发者手册归档](/developer/devdocs/archives.html)[开发者手册 Section 归档](/developer/devdocs/sections_p1.html)

Copyright © 2013 - 2026 Tencent Cloud.

All Rights Reserved. 腾讯云 版权所有

登录 后参与评论

000推荐

if (!String.prototype.replaceAll) {
String.prototype.replaceAll = function (str, newStr) {
// If a regex pattern
if (Object.prototype.toString.call(str).toLowerCase() === '[object regexp]') {
return this.replace(str, newStr);
}
// If a string
return this.replace(new RegExp(str, 'g'), newStr);
};
}
{"props":{"isMobile":false,"isSupportWebp":false,"currentDomain":"cloud.tencent.com","baseUrl":"https://cloud.tencent.com","reqId":"6YF\_WYicUmFumhno3cbcu","query":{"articleId":"2636348"},"platform":"other","env":"production","\_\_N\_SSP":true,"pageProps":{"fallback":{"#url:\"/api/article/detail\",params:#articleId:2636348,,":{"articleData":{"articleId":2636348,"codeLineNum":554,"readingTime":146,"wordsNum":673},"articleInfo":{"articleId":2636348,"channel":2,"commentNum":0,"content":{"blocks":[{"key":"fuie1","text":"AI提示词是与AI工具进行有效沟通的关键，合适的提示词可以显著提升代码生成质量和开发效率。","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"89g2e","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"16pp3","text":"介绍","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E4%BB%8B%E7%BB%8D"}},{"key":"20ehr","text":"  随着AI编程助手的普及，提示词工程（Prompt Engineering）已成为现代开发者的重要技能。在前端开发中，合适的AI提示词可以帮助我们快速生成高质量的代码、解决复杂的技术问题、进行代码审查和性能优化。本文将系统整理前端开发中常用的AI提示词，按功能场景分类，为开发者提供实用的参考指南。","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"cj7tv","text":"代码生成类提示词","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90%E7%B1%BB%E6%8F%90%E7%A4%BA%E8%AF%8D"}},{"key":"8480e","text":"React组件生成","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"React%E7%BB%84%E4%BB%B6%E7%94%9F%E6%88%90"}},{"key":"devhr","text":"# 生成React函数组件\n\n## 基础组件生成\n~~~\nCreate a React functional component that [describe functionality].\nThe component should use TypeScript and follow React best practices.\nInclude proper TypeScript interfaces for props.\nAdd JSDoc comments for exported functions and components.\n~~~\n\n## 复杂组件生成\n~~~\nCreate a [component name] component with the following requirements:\n- Use React hooks (useState, useEffect, etc.)\n- Include proper TypeScript types\n- Follow accessibility guidelines (WCAG 2.1 AA)\n- Support dark/light theme\n- Include loading and error states\n- Use modern React patterns (compound components, render props, etc.)\n\nComponent specification:\n- [specific requirements]\n- [styling framework] for styling\n- [additional functionality]\n~~~\n\n## 自定义Hook生成\n~~~\nCreate a custom React hook called use[HookName] that:\n- Purpose: [describe what the hook does]\n- Parameters: [describe input parameters]\n- Return value: [describe return value]\n- Side effects: [describe any side effects]\n- Dependencies: [list external dependencies if any]\n\nInclude proper TypeScript typing and error handling.\nAdd comprehensive JSDoc documentation.\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"av4sv","text":"Vue组件生成","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"Vue%E7%BB%84%E4%BB%B6%E7%94%9F%E6%88%90"}},{"key":"ccff2","text":"# Vue组件生成提示词\n\n## Composition API组件\n~~~\nCreate a Vue 3 component using Composition API that [functionality description].\nUse TypeScript and follow Vue 3 best practices.\n\nComponent requirements:\n- Props: [list required props with types]\n- Emits: [list emitted events]\n- Slots: [describe slots if needed]\n- Exposed methods: [methods to expose]\n\nInclude proper TypeScript interfaces and generic typing where appropriate.\nUse provide/inject for parent-child communication if needed.\n~~~\n\n## Vue组件优化\n~~~\nRefactor the following Vue component to improve performance and maintainability:\n- Convert Options API to Composition API\n- Optimize reactivity using ref/computed properly\n- Add proper TypeScript typing\n- Implement proper error handling\n- Add loading states and error boundaries\n- Follow Vue style guide recommendations\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"4boob","text":"CSS/样式生成","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"CSS/%E6%A0%B7%E5%BC%8F%E7%94%9F%E6%88%90"}},{"key":"65rrr","text":"# CSS样式生成提示词\n\n## TailwindCSS组件\n~~~\nCreate a responsive [component name] component using TailwindCSS.\nThe component should:\n- Be fully responsive (mobile, tablet, desktop)\n- Follow accessibility best practices\n- Include dark mode support\n- Use Tailwind's utility classes efficiently\n- Be customizable with props/config\n\nStyle requirements:\n- [specific color scheme]\n- [typography requirements]\n- [animation/transitions if needed]\n- [layout constraints]\n~~~\n\n## 动画效果生成\n~~~\nCreate CSS animations for [describe animation purpose].\nProvide both pure CSS (using @keyframes) and TailwindCSS implementations.\nInclude:\n- Smooth transitions\n- Performance optimizations (using transform, opacity)\n- Responsive behavior\n- Accessibility considerations (prefers-reduced-motion)\n- Cross-browser compatibility notes\n~~~\n\n## 复杂布局生成\n~~~\nCreate a complex responsive layout using CSS Grid and Flexbox that:\n- Has [number] columns on desktop, [number] on tablet, [number] on mobile\n- Maintains aspect ratios for images/media\n- Handles content overflow gracefully\n- Supports RTL languages\n- Optimizes for SEO and accessibility\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"2ni39","text":"代码优化类提示词","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E4%BB%A3%E7%A0%81%E4%BC%98%E5%8C%96%E7%B1%BB%E6%8F%90%E7%A4%BA%E8%AF%8D"}},{"key":"f584g","text":"性能优化","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96"}},{"key":"5f8hr","text":"# 性能优化提示词\n\n## 代码性能优化\n~~~\nAnalyze and optimize the following code for performance:\n- Identify performance bottlenecks\n- Suggest React memoization strategies\n- Optimize rendering with React.memo, useMemo, useCallback\n- Implement code splitting and lazy loading\n- Optimize bundle size\n- Suggest algorithm improvements\n- Identify unnecessary re-renders\n\nProvide specific recommendations with code examples.\n~~~\n\n## 前端性能优化\n~~~\nImplement performance optimizations for a React application:\n- Code splitting strategies\n- Image optimization techniques\n- Caching mechanisms\n- Bundle size reduction\n- Loading state optimizations\n- Memory leak prevention\n- Network request optimization\n\nProvide specific implementation examples for each technique.\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"bv0ne","text":"代码重构","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E4%BB%A3%E7%A0%81%E9%87%8D%E6%9E%84"}},{"key":"5jdai","text":"# 代码重构提示词\n\n## 重构建议\n~~~\nRefactor the following code to improve:\n- Readability and maintainability\n- Performance\n- Type safety (add TypeScript if missing)\n- Error handling\n- Testing strategy\n- Separation of concerns\n- Modern JavaScript/React patterns\n\nKeep the same functionality but improve the code structure and quality.\n~~~\n\n## 从Class组件到Hook组件\n~~~\nConvert the following React class component to a functional component using hooks:\n- Replace lifecycle methods with useEffect hooks\n- Convert state management to useState/useReducer\n- Handle refs appropriately\n- Maintain the same functionality\n- Add proper TypeScript typing\n- Include proper cleanup functions\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"eo37j","text":"调试与问题解决","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E8%B0%83%E8%AF%95%E4%B8%8E%E9%97%AE%E9%A2%98%E8%A7%A3%E5%86%B3"}},{"key":"68o6m","text":"错误排查","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E9%94%99%E8%AF%AF%E6%8E%92%E6%9F%A5"}},{"key":"3kba8","text":"# 调试提示词\n\n## 错误诊断\n~~~\nThe following code is throwing [error message]. Please analyze the code and:\n1. Identify the root cause of the error\n2. Explain why this error occurs\n3. Provide the corrected code\n4. Explain the fix and why it works\n5. Suggest similar errors to watch out for\n\nCode:\n[insert problematic code here]\n~~~\n\n## 性能问题诊断\n~~~\nThe application is experiencing [performance issue description]. Please help diagnose and fix:\n1. Identify potential causes\n2. Suggest debugging tools to use\n3. Provide code improvements\n4. Recommend performance monitoring solutions\n5. Estimate performance gains\n\nCurrent symptoms:\n- [list symptoms]\n- [performance metrics if available]\n- [user impact]\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"6dr5o","text":"代码审查","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E4%BB%A3%E7%A0%81%E5%AE%A1%E6%9F%A5"}},{"key":"43b98","text":"# 代码审查提示词\n\n## 安全审查\n~~~\nReview the following code for security vulnerabilities:\n- XSS prevention\n- CSRF protection\n- Input validation\n- Sanitization practices\n- Authentication/authorization issues\n- Data exposure risks\n- Third-party library security\n\nProvide specific fixes for each vulnerability found.\n~~~\n\n## 质量审查\n~~~\nPerform a comprehensive code review focusing on:\n- Code quality and readability\n- Best practices adherence\n- Potential bugs\n- Performance considerations\n- Maintainability\n- Documentation completeness\n- Test coverage suggestions\n\nRate each issue by severity and provide improvement suggestions.\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"e0ep4","text":"国际化与多语言","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%9B%BD%E9%99%85%E5%8C%96%E4%B8%8E%E5%A4%9A%E8%AF%AD%E8%A8%80"}},{"key":"bb8ho","text":"I18n实现","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"I18n%E5%AE%9E%E7%8E%B0"}},{"key":"6u0eb","text":"# 国际化提示词\n\n## 多语言支持\n~~~\nImplement internationalization (i18n) for the following React application:\n- Use react-i18next or next-i18next\n- Create language switcher component\n- Implement RTL support where needed\n- Handle pluralization\n- Manage date/time formatting\n- Handle number/currency formatting\n- Organize translation files structure\n- Implement fallback languages\n\nInclude proper TypeScript typing for translations.\n~~~\n\n## 翻译文件生成\n~~~\nCreate translation files for [language] localization:\n- Extract translatable strings from [provided code]\n- Organize translations by domain/context\n- Handle pluralization\n- Include RTL language considerations\n- Follow linguistic best practices\n- Maintain consistency across translations\n\nProvide both JSON structure and example translations.\n~~~\n\n## 日期时间国际化\n~~~\nImplement internationalized date and time formatting that:\n- Uses user's locale automatically\n- Handles different calendar systems\n- Manages time zones properly\n- Supports 12/24-hour formats\n- Handles relative time (e.g., \"2 hours ago\")\n- Includes proper TypeScript types\n\nUse modern JavaScript Internationalization API.\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"2g7ca","text":"测试相关","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E6%B5%8B%E8%AF%95%E7%9B%B8%E5%85%B3"}},{"key":"ebrk8","text":"单元测试生成","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95%E7%94%9F%E6%88%90"}},{"key":"b4ihh","text":"# 测试生成提示词\n\n## React组件测试\n~~~\nCreate comprehensive unit tests for the following React component using:\n- Testing Library and React Testing Library\n- Jest for test runner\n- TypeScript support\n\nTest requirements:\n- Render with different props\n- Handle user interactions\n- Test async behavior\n- Mock external dependencies\n- Test edge cases\n- Accessibility testing\n- Snapshot testing if appropriate\n~~~\n\n## API测试\n~~~\nCreate API tests for the following endpoints:\n- Test successful responses\n- Test error scenarios\n- Validate response schemas\n- Test authentication/authorization\n- Handle different HTTP methods\n- Test rate limiting\n- Performance testing scenarios\n- Include both happy path and error cases\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"9odq","text":"测试优化","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E6%B5%8B%E8%AF%95%E4%BC%98%E5%8C%96"}},{"key":"fprba","text":"# 测试优化提示词\n\n## 测试重构\n~~~\nRefactor the following tests to improve:\n- Test structure and organization\n- Readability and maintainability\n- Performance and speed\n- Coverage and effectiveness\n- Mock management\n- Test data management\n- Error handling in tests\n\nMaintain test effectiveness while improving quality.\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"117b1","text":"工具与配置","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%B7%A5%E5%85%B7%E4%B8%8E%E9%85%8D%E7%BD%AE"}},{"key":"4mtbt","text":"开发工具配置","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7%E9%85%8D%E7%BD%AE"}},{"key":"5jj89","text":"# 工具配置提示词\n\n## ESLint/Prettier配置\n~~~\nCreate ESLint and Prettier configuration for a modern React project that:\n- Enforces React best practices\n- Includes TypeScript support\n- Follows Airbnb or similar style guide\n- Includes React Hooks rules\n- Enforces import ordering\n- Includes testing library rules\n- Optimizes for VS Code integration\n- Provides auto-fix capabilities\n\nProvide both base configuration and React-specific extensions.\n~~~\n\n## 构建工具配置\n~~~\nConfigure Vite for a React project with the following requirements:\n- TypeScript support\n- CSS preprocessing (SASS/SCSS)\n- Asset optimization\n- Environment variables\n- Proxy configuration for API\n- Code splitting setup\n- Production optimization\n- Development server configuration\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"f9cej","text":"文档与注释","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E6%96%87%E6%A1%A3%E4%B8%8E%E6%B3%A8%E9%87%8A"}},{"key":"89mip","text":"代码文档","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E4%BB%A3%E7%A0%81%E6%96%87%E6%A1%A3"}},{"key":"8cg9a","text":"# 文档生成提示词\n\n## JSDoc生成\n~~~\nGenerate comprehensive JSDoc documentation for the following code:\n- Function/method descriptions\n- Parameter types and descriptions\n- Return value documentation\n- Exception/error documentation\n- Example usage\n- Accessibility considerations\n- Performance implications\n- Deprecation notices if applicable\n~~~\n\n## API文档\n~~~\nCreate API documentation for the following REST endpoints:\n- Request/response schemas\n- Authentication requirements\n- Error response formats\n- Rate limiting information\n- Example requests/responses\n- Curl commands\n- SDK usage examples\n- Security considerations\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"ala6m","text":"AI辅助开发工作流","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"AI%E8%BE%85%E5%8A%A9%E5%BC%80%E5%8F%91%E5%B7%A5%E4%BD%9C%E6%B5%81"}},{"key":"824ji","text":"提示词优化策略","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%BC%98%E5%8C%96%E7%AD%96%E7%95%A5"}},{"key":"2tmj7","text":"# 提示词优化策略\n\n## 提示词结构\n~~~\nEffective AI prompt structure for code generation:\n\n1. Role Definition: \"Act as an experienced React/JavaScript developer\"\n2. Task Definition: \"Create a component that...\"\n3. Constraints: \"Use TypeScript, follow accessibility...\"\n4. Examples: \"Similar to X, but with Y functionality\"\n5. Output Format: \"Return code with comments and documentation\"\n~~~\n\n## 上下文提供\n~~~\nWhen providing context to AI:\n\n- Share relevant code snippets\n- Explain business requirements\n- Specify technical constraints\n- Mention performance requirements\n- Indicate design system components\n- Reference existing patterns\n- Clarify edge cases\n- Specify testing requirements\n~~~\n\n## 反量反馈循环\n~~~\nIterative improvement with AI:\n\n1. Start with high-level requirements\n2. Review initial output\n3. Provide specific feedback\n4. Request targeted improvements\n5. Validate against requirements\n6. Repeat until satisfied\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"c9ae0","text":"常见场景专用提示词","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%B8%B8%E8%A7%81%E5%9C%BA%E6%99%AF%E4%B8%93%E7%94%A8%E6%8F%90%E7%A4%BA%E8%AF%8D"}},{"key":"6fpqg","text":"响应式设计","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%93%8D%E5%BA%94%E5%BC%8F%E8%AE%BE%E8%AE%A1"}},{"key":"ek1dd","text":"# 响应式设计提示词\n\n## 移动优先设计\n~~~\nCreate a mobile-first responsive component that:\n- Starts with mobile layout\n- Progressively enhances for larger screens\n- Uses appropriate media query breakpoints\n- Maintains touch-friendly interactions\n- Optimizes for mobile performance\n- Considers mobile-specific UX patterns\n- Follows mobile accessibility guidelines\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"6i4ri","text":"可访问性","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%8F%AF%E8%AE%BF%E9%97%AE%E6%80%A7"}},{"key":"c8i7k","text":"# 可访问性提示词\n\n## WCAG合规\n~~~\nCreate an accessible component that complies with WCAG 2.1 AA guidelines:\n- Proper heading structure\n- Sufficient color contrast\n- Keyboard navigation support\n- Screen reader compatibility\n- Focus management\n- ARIA attributes where needed\n- Alternative text for images\n- Form accessibility\n- Skip links for navigation\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"2a6i1","text":"安全编程","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%AE%89%E5%85%A8%E7%BC%96%E7%A8%8B"}},{"key":"6ee9a","text":"# 安全编程提示词\n\n## 输入验证\n~~~\nImplement robust input validation for [specific input type] that:\n- Validates data type and format\n- Implements sanitization\n- Prevents injection attacks\n- Handles edge cases\n- Provides user-friendly error messages\n- Maintains good UX while being secure\n- Includes both client and server validation\n~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"2183j","text":"实用提示词模板","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%AE%9E%E7%94%A8%E6%8F%90%E7%A4%BA%E8%AF%8D%E6%A8%A1%E6%9D%BF"}},{"key":"5c206","text":"通用代码生成模板","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E9%80%9A%E7%94%A8%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90%E6%A8%A1%E6%9D%BF"}},{"key":"7dj38","text":"# 通用模板\n\n~~~~\nAs an experienced [technology] developer, create [component/type] that:\nPURPOSE: [what the code should accomplish]\nREQUIREMENTS: [specific technical requirements]\nCONSTRAINTS: [limitations or specific constraints]\nTECHNOLOGY\_STACK: [languages, frameworks, libraries]\nPERFORMANCE: [speed, bundle size, etc. requirements]\nACCESSIBILITY: [compliance level required]\nTESTING: [test coverage expectations]\n\nInclude:\n- Proper TypeScript definitions if applicable\n- Comprehensive error handling\n- Performance optimizations\n- Security best practices\n- Accessibility features\n- Documentation and comments\n- Usage examples\n\nReturn production-ready code following industry best practices.\n~~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"6kjck","text":"调试求助模板","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E8%B0%83%E8%AF%95%E6%B1%82%E5%8A%A9%E6%A8%A1%E6%9D%BF"}},{"key":"acsi2","text":"# 调试模板\n\n~~~~\nI'm experiencing [specific problem] with the following code:\n[provide code snippet]\n\nEXPECTED\_BEHAVIOR: [what should happen]\nACTUAL\_BEHAVIOR: [what is happening]\nERROR\_MESSAGES: [any error messages]\nCONTEXT: [environment, browser, dependencies]\n\nPlease help me:\n1. Identify the root cause\n2. Provide a solution\n3. Explain why the issue occurred\n4. Suggest how to prevent similar issues\n5. Recommend debugging tools/techniques for similar problems\n\nConsider [specific constraints or requirements].\n~~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"si8q","text":"多语言翻译助手模板","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E5%A4%9A%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91%E5%8A%A9%E6%89%8B%E6%A8%A1%E6%9D%BF"}},{"key":"bfjoo","text":"# 多语言翻译助手\n\n## 翻译助手角色\n~~~~\nAct as a professional translator. I will provide multiple texts separated by newlines. Translate each text into multiple languages and return the results in JSON format.\n\nLanguages to translate to:\n- zh\_CN: Simplified Chinese\n- en\_US: English\n- ja\_JP: Japanese\n- ko\_KR: Korean\n- fr\_FR: French\n- de\_DE: German\n- es\_ES: Spanish\n- ar\_SA: Arabic\n- pt\_BR: Portuguese (Brazil)\n- ru\_RU: Russian\n- it\_IT: Italian\n- th\_TH: Thai\n\nInput format:\n[Line 1 - text to translate]\n[Line 2 - another text to translate]\n[Line 3 - more text to translate]\n\nOutput format:\n~~~\n[\n { \"lang\": \"zh\_CN\", \"name\": \"中文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"en\_US\", \"name\": \"英文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ja\_JP\", \"name\": \"日文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ko\_KR\", \"name\": \"韩文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"fr\_FR\", \"name\": \"法文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"de\_DE\", \"name\": \"德文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"es\_ES\", \"name\": \"西班牙文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ar\_SA\", \"name\": \"阿拉伯文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"pt\_BR\", \"name\": \"葡萄牙文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ru\_RU\", \"name\": \"俄文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"it\_IT\", \"name\": \"意大利文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"th\_TH\", \"name\": \"泰文\", \"text\": \"[translated text for line 1]\" }\n]\n~~~\n\n[Continue with translations for each input line...]\n\nExample input:\nData Table Configuration\nUser Profile Management\nReal-time Analytics Dashboard\n\nExample output:\n~~~\n[\n { \"lang\": \"zh\_CN\", \"name\": \"中文\", \"text\": \"数据表配置\" },\n { \"lang\": \"en\_US\", \"name\": \"英文\", \"text\": \"Data Table Configuration\" },\n { \"lang\": \"ja\_JP\", \"name\": \"日文\", \"text\": \"データテーブル構成\" },\n { \"lang\": \"ko\_KR\", \"name\": \"韩文\", \"text\": \"데이터 테이블 구성\" },\n { \"lang\": \"fr\_FR\", \"name\": \"法文\", \"text\": \"Configuration du tableau de données\" },\n { \"lang\": \"de\_DE\", \"name\": \"德文\", \"text\": \"Datentabellenkonfiguration\" },\n { \"lang\": \"es\_ES\", \"name\": \"西班牙文\", \"text\": \"Configuración de tabla de datos\" },\n { \"lang\": \"ar\_SA\", \"name\": \"阿拉伯文\", \"text\": \"تكوين جدول البيانات\" },\n { \"lang\": \"pt\_BR\", \"name\": \"葡萄牙文\", \"text\": \"Configuração da tabela de dados\" },\n { \"lang\": \"ru\_RU\", \"name\": \"俄文\", \"text\": \"Конфигурация таблицы данных\" },\n { \"lang\": \"it\_IT\", \"name\": \"意大利文\", \"text\": \"Configurazione tabella dati\" },\n { \"lang\": \"th\_TH\", \"name\": \"泰文\", \"text\": \"การกำหนดค่าตารางข้อมูล\" }\n]\n~~~\n\nMaintain accurate terminology and cultural appropriateness in each language.\n~~~~","type":"code-block","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"syntax":"javascript","languageByAi":"javascript"}},{"key":"j49l","text":"有效的AI提示词应该具体、清晰且包含足够的上下文信息。通过使用结构化的提示词模板，可以获得更准确、更符合需求的AI输出。","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"3i5pl","text":"总结","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{"text":"%E6%80%BB%E7%BB%93"}},{"key":"4ujj2","text":"  AI提示词是现代前端开发的重要工具，掌握有效的提示词技巧可以显著提升开发效率和代码质量。关键要点包括：","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bjmp","text":"明确目标：清楚描述需要生成的代码功能和特性","type":"ordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":4,"style":"BOLD"}],"entityRanges":[],"data":{}},{"key":"bme5d","text":"提供上下文：包含技术栈、约束条件、性能要求等信息","type":"ordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":5,"style":"BOLD"}],"entityRanges":[],"data":{}},{"key":"5a9fr","text":"结构化组织：使用清晰的结构化格式提高AI理解能力","type":"ordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":5,"style":"BOLD"}],"entityRanges":[],"data":{}},{"key":"3sepb","text":"迭代优化：根据AI输出进行调整和优化","type":"ordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":4,"style":"BOLD"}],"entityRanges":[],"data":{}},{"key":"2k72","text":"质量检查：始终审查AI生成的代码确保质量和安全性","type":"ordered-list-item","depth":0,"inlineStyleRanges":[{"offset":0,"length":4,"style":"BOLD"}],"entityRanges":[],"data":{}},{"key":"aeubk","text":"  随着AI技术的不断发展，提示词工程将成为前端开发者的核心技能之一。通过不断练习和优化提示词策略，开发者可以更有效地利用AI工具提升工作效率。","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{},"sourceHash":715426688},"createTime":1773136087,"ext":{"closeTextLink":0,"comment\_ban":0,"description":"","focusRead":0},"favNum":0,"html":"","isOriginal":0,"likeNum":1,"pic":"","plain":"AI提示词是与AI工具进行有效沟通的关键，合适的提示词可以显著提升代码生成质量和开发效率。\n介绍\n  随着AI编程助手的普及，提示词工程（Prompt Engineering）已成为现代开发者的重要技能。在前端开发中，合适的AI提示词可以帮助我们快速生成高质量的代码、解决复杂的技术问题、进行代码审查和性能优化。本文将系统整理前端开发中常用的AI提示词，按功能场景分类，为开发者提供实用的参考指南。\n代码生成类提示词\nReact组件生成\n# 生成React函数组件\n\n## 基础组件生成\n~~~\nCreate a React functional component that [describe functionality].\nThe component should use TypeScript and follow React best practices.\nInclude proper TypeScript interfaces for props.\nAdd JSDoc comments for exported functions and components.\n~~~\n\n## 复杂组件生成\n~~~\nCreate a [component name] component with the following requirements:\n- Use React hooks (useState, useEffect, etc.)\n- Include proper TypeScript types\n- Follow accessibility guidelines (WCAG 2.1 AA)\n- Support dark/light theme\n- Include loading and error states\n- Use modern React patterns (compound components, render props, etc.)\n\nComponent specification:\n- [specific requirements]\n- [styling framework] for styling\n- [additional functionality]\n~~~\n\n## 自定义Hook生成\n~~~\nCreate a custom React hook called use[HookName] that:\n- Purpose: [describe what the hook does]\n- Parameters: [describe input parameters]\n- Return value: [describe return value]\n- Side effects: [describe any side effects]\n- Dependencies: [list external dependencies if any]\n\nInclude proper TypeScript typing and error handling.\nAdd comprehensive JSDoc documentation.\n~~~\nVue组件生成\n# Vue组件生成提示词\n\n## Composition API组件\n~~~\nCreate a Vue 3 component using Composition API that [functionality description].\nUse TypeScript and follow Vue 3 best practices.\n\nComponent requirements:\n- Props: [list required props with types]\n- Emits: [list emitted events]\n- Slots: [describe slots if needed]\n- Exposed methods: [methods to expose]\n\nInclude proper TypeScript interfaces and generic typing where appropriate.\nUse provide/inject for parent-child communication if needed.\n~~~\n\n## Vue组件优化\n~~~\nRefactor the following Vue component to improve performance and maintainability:\n- Convert Options API to Composition API\n- Optimize reactivity using ref/computed properly\n- Add proper TypeScript typing\n- Implement proper error handling\n- Add loading states and error boundaries\n- Follow Vue style guide recommendations\n~~~\nCSS/样式生成\n# CSS样式生成提示词\n\n## TailwindCSS组件\n~~~\nCreate a responsive [component name] component using TailwindCSS.\nThe component should:\n- Be fully responsive (mobile, tablet, desktop)\n- Follow accessibility best practices\n- Include dark mode support\n- Use Tailwind's utility classes efficiently\n- Be customizable with props/config\n\nStyle requirements:\n- [specific color scheme]\n- [typography requirements]\n- [animation/transitions if needed]\n- [layout constraints]\n~~~\n\n## 动画效果生成\n~~~\nCreate CSS animations for [describe animation purpose].\nProvide both pure CSS (using @keyframes) and TailwindCSS implementations.\nInclude:\n- Smooth transitions\n- Performance optimizations (using transform, opacity)\n- Responsive behavior\n- Accessibility considerations (prefers-reduced-motion)\n- Cross-browser compatibility notes\n~~~\n\n## 复杂布局生成\n~~~\nCreate a complex responsive layout using CSS Grid and Flexbox that:\n- Has [number] columns on desktop, [number] on tablet, [number] on mobile\n- Maintains aspect ratios for images/media\n- Handles content overflow gracefully\n- Supports RTL languages\n- Optimizes for SEO and accessibility\n~~~\n代码优化类提示词\n性能优化\n# 性能优化提示词\n\n## 代码性能优化\n~~~\nAnalyze and optimize the following code for performance:\n- Identify performance bottlenecks\n- Suggest React memoization strategies\n- Optimize rendering with React.memo, useMemo, useCallback\n- Implement code splitting and lazy loading\n- Optimize bundle size\n- Suggest algorithm improvements\n- Identify unnecessary re-renders\n\nProvide specific recommendations with code examples.\n~~~\n\n## 前端性能优化\n~~~\nImplement performance optimizations for a React application:\n- Code splitting strategies\n- Image optimization techniques\n- Caching mechanisms\n- Bundle size reduction\n- Loading state optimizations\n- Memory leak prevention\n- Network request optimization\n\nProvide specific implementation examples for each technique.\n~~~\n代码重构\n# 代码重构提示词\n\n## 重构建议\n~~~\nRefactor the following code to improve:\n- Readability and maintainability\n- Performance\n- Type safety (add TypeScript if missing)\n- Error handling\n- Testing strategy\n- Separation of concerns\n- Modern JavaScript/React patterns\n\nKeep the same functionality but improve the code structure and quality.\n~~~\n\n## 从Class组件到Hook组件\n~~~\nConvert the following React class component to a functional component using hooks:\n- Replace lifecycle methods with useEffect hooks\n- Convert state management to useState/useReducer\n- Handle refs appropriately\n- Maintain the same functionality\n- Add proper TypeScript typing\n- Include proper cleanup functions\n~~~\n调试与问题解决\n错误排查\n# 调试提示词\n\n## 错误诊断\n~~~\nThe following code is throwing [error message]. Please analyze the code and:\n1. Identify the root cause of the error\n2. Explain why this error occurs\n3. Provide the corrected code\n4. Explain the fix and why it works\n5. Suggest similar errors to watch out for\n\nCode:\n[insert problematic code here]\n~~~\n\n## 性能问题诊断\n~~~\nThe application is experiencing [performance issue description]. Please help diagnose and fix:\n1. Identify potential causes\n2. Suggest debugging tools to use\n3. Provide code improvements\n4. Recommend performance monitoring solutions\n5. Estimate performance gains\n\nCurrent symptoms:\n- [list symptoms]\n- [performance metrics if available]\n- [user impact]\n~~~\n代码审查\n# 代码审查提示词\n\n## 安全审查\n~~~\nReview the following code for security vulnerabilities:\n- XSS prevention\n- CSRF protection\n- Input validation\n- Sanitization practices\n- Authentication/authorization issues\n- Data exposure risks\n- Third-party library security\n\nProvide specific fixes for each vulnerability found.\n~~~\n\n## 质量审查\n~~~\nPerform a comprehensive code review focusing on:\n- Code quality and readability\n- Best practices adherence\n- Potential bugs\n- Performance considerations\n- Maintainability\n- Documentation completeness\n- Test coverage suggestions\n\nRate each issue by severity and provide improvement suggestions.\n~~~\n国际化与多语言\nI18n实现\n# 国际化提示词\n\n## 多语言支持\n~~~\nImplement internationalization (i18n) for the following React application:\n- Use react-i18next or next-i18next\n- Create language switcher component\n- Implement RTL support where needed\n- Handle pluralization\n- Manage date/time formatting\n- Handle number/currency formatting\n- Organize translation files structure\n- Implement fallback languages\n\nInclude proper TypeScript typing for translations.\n~~~\n\n## 翻译文件生成\n~~~\nCreate translation files for [language] localization:\n- Extract translatable strings from [provided code]\n- Organize translations by domain/context\n- Handle pluralization\n- Include RTL language considerations\n- Follow linguistic best practices\n- Maintain consistency across translations\n\nProvide both JSON structure and example translations.\n~~~\n\n## 日期时间国际化\n~~~\nImplement internationalized date and time formatting that:\n- Uses user's locale automatically\n- Handles different calendar systems\n- Manages time zones properly\n- Supports 12/24-hour formats\n- Handles relative time (e.g., \"2 hours ago\")\n- Includes proper TypeScript types\n\nUse modern JavaScript Internationalization API.\n~~~\n测试相关\n单元测试生成\n# 测试生成提示词\n\n## React组件测试\n~~~\nCreate comprehensive unit tests for the following React component using:\n- Testing Library and React Testing Library\n- Jest for test runner\n- TypeScript support\n\nTest requirements:\n- Render with different props\n- Handle user interactions\n- Test async behavior\n- Mock external dependencies\n- Test edge cases\n- Accessibility testing\n- Snapshot testing if appropriate\n~~~\n\n## API测试\n~~~\nCreate API tests for the following endpoints:\n- Test successful responses\n- Test error scenarios\n- Validate response schemas\n- Test authentication/authorization\n- Handle different HTTP methods\n- Test rate limiting\n- Performance testing scenarios\n- Include both happy path and error cases\n~~~\n测试优化\n# 测试优化提示词\n\n## 测试重构\n~~~\nRefactor the following tests to improve:\n- Test structure and organization\n- Readability and maintainability\n- Performance and speed\n- Coverage and effectiveness\n- Mock management\n- Test data management\n- Error handling in tests\n\nMaintain test effectiveness while improving quality.\n~~~\n工具与配置\n开发工具配置\n# 工具配置提示词\n\n## ESLint/Prettier配置\n~~~\nCreate ESLint and Prettier configuration for a modern React project that:\n- Enforces React best practices\n- Includes TypeScript support\n- Follows Airbnb or similar style guide\n- Includes React Hooks rules\n- Enforces import ordering\n- Includes testing library rules\n- Optimizes for VS Code integration\n- Provides auto-fix capabilities\n\nProvide both base configuration and React-specific extensions.\n~~~\n\n## 构建工具配置\n~~~\nConfigure Vite for a React project with the following requirements:\n- TypeScript support\n- CSS preprocessing (SASS/SCSS)\n- Asset optimization\n- Environment variables\n- Proxy configuration for API\n- Code splitting setup\n- Production optimization\n- Development server configuration\n~~~\n文档与注释\n代码文档\n# 文档生成提示词\n\n## JSDoc生成\n~~~\nGenerate comprehensive JSDoc documentation for the following code:\n- Function/method descriptions\n- Parameter types and descriptions\n- Return value documentation\n- Exception/error documentation\n- Example usage\n- Accessibility considerations\n- Performance implications\n- Deprecation notices if applicable\n~~~\n\n## API文档\n~~~\nCreate API documentation for the following REST endpoints:\n- Request/response schemas\n- Authentication requirements\n- Error response formats\n- Rate limiting information\n- Example requests/responses\n- Curl commands\n- SDK usage examples\n- Security considerations\n~~~\nAI辅助开发工作流\n提示词优化策略\n# 提示词优化策略\n\n## 提示词结构\n~~~\nEffective AI prompt structure for code generation:\n\n1. Role Definition: \"Act as an experienced React/JavaScript developer\"\n2. Task Definition: \"Create a component that...\"\n3. Constraints: \"Use TypeScript, follow accessibility...\"\n4. Examples: \"Similar to X, but with Y functionality\"\n5. Output Format: \"Return code with comments and documentation\"\n~~~\n\n## 上下文提供\n~~~\nWhen providing context to AI:\n\n- Share relevant code snippets\n- Explain business requirements\n- Specify technical constraints\n- Mention performance requirements\n- Indicate design system components\n- Reference existing patterns\n- Clarify edge cases\n- Specify testing requirements\n~~~\n\n## 反量反馈循环\n~~~\nIterative improvement with AI:\n\n1. Start with high-level requirements\n2. Review initial output\n3. Provide specific feedback\n4. Request targeted improvements\n5. Validate against requirements\n6. Repeat until satisfied\n~~~\n常见场景专用提示词\n响应式设计\n# 响应式设计提示词\n\n## 移动优先设计\n~~~\nCreate a mobile-first responsive component that:\n- Starts with mobile layout\n- Progressively enhances for larger screens\n- Uses appropriate media query breakpoints\n- Maintains touch-friendly interactions\n- Optimizes for mobile performance\n- Considers mobile-specific UX patterns\n- Follows mobile accessibility guidelines\n~~~\n可访问性\n# 可访问性提示词\n\n## WCAG合规\n~~~\nCreate an accessible component that complies with WCAG 2.1 AA guidelines:\n- Proper heading structure\n- Sufficient color contrast\n- Keyboard navigation support\n- Screen reader compatibility\n- Focus management\n- ARIA attributes where needed\n- Alternative text for images\n- Form accessibility\n- Skip links for navigation\n~~~\n安全编程\n# 安全编程提示词\n\n## 输入验证\n~~~\nImplement robust input validation for [specific input type] that:\n- Validates data type and format\n- Implements sanitization\n- Prevents injection attacks\n- Handles edge cases\n- Provides user-friendly error messages\n- Maintains good UX while being secure\n- Includes both client and server validation\n~~~\n实用提示词模板\n通用代码生成模板\n# 通用模板\n\n~~~~\nAs an experienced [technology] developer, create [component/type] that:\nPURPOSE: [what the code should accomplish]\nREQUIREMENTS: [specific technical requirements]\nCONSTRAINTS: [limitations or specific constraints]\nTECHNOLOGY\_STACK: [languages, frameworks, libraries]\nPERFORMANCE: [speed, bundle size, etc. requirements]\nACCESSIBILITY: [compliance level required]\nTESTING: [test coverage expectations]\n\nInclude:\n- Proper TypeScript definitions if applicable\n- Comprehensive error handling\n- Performance optimizations\n- Security best practices\n- Accessibility features\n- Documentation and comments\n- Usage examples\n\nReturn production-ready code following industry best practices.\n~~~~\n调试求助模板\n# 调试模板\n\n~~~~\nI'm experiencing [specific problem] with the following code:\n[provide code snippet]\n\nEXPECTED\_BEHAVIOR: [what should happen]\nACTUAL\_BEHAVIOR: [what is happening]\nERROR\_MESSAGES: [any error messages]\nCONTEXT: [environment, browser, dependencies]\n\nPlease help me:\n1. Identify the root cause\n2. Provide a solution\n3. Explain why the issue occurred\n4. Suggest how to prevent similar issues\n5. Recommend debugging tools/techniques for similar problems\n\nConsider [specific constraints or requirements].\n~~~~\n多语言翻译助手模板\n# 多语言翻译助手\n\n## 翻译助手角色\n~~~~\nAct as a professional translator. I will provide multiple texts separated by newlines. Translate each text into multiple languages and return the results in JSON format.\n\nLanguages to translate to:\n- zh\_CN: Simplified Chinese\n- en\_US: English\n- ja\_JP: Japanese\n- ko\_KR: Korean\n- fr\_FR: French\n- de\_DE: German\n- es\_ES: Spanish\n- ar\_SA: Arabic\n- pt\_BR: Portuguese (Brazil)\n- ru\_RU: Russian\n- it\_IT: Italian\n- th\_TH: Thai\n\nInput format:\n[Line 1 - text to translate]\n[Line 2 - another text to translate]\n[Line 3 - more text to translate]\n\nOutput format:\n~~~\n[\n { \"lang\": \"zh\_CN\", \"name\": \"中文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"en\_US\", \"name\": \"英文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ja\_JP\", \"name\": \"日文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ko\_KR\", \"name\": \"韩文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"fr\_FR\", \"name\": \"法文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"de\_DE\", \"name\": \"德文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"es\_ES\", \"name\": \"西班牙文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ar\_SA\", \"name\": \"阿拉伯文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"pt\_BR\", \"name\": \"葡萄牙文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"ru\_RU\", \"name\": \"俄文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"it\_IT\", \"name\": \"意大利文\", \"text\": \"[translated text for line 1]\" },\n { \"lang\": \"th\_TH\", \"name\": \"泰文\", \"text\": \"[translated text for line 1]\" }\n]\n~~~\n\n[Continue with translations for each input line...]\n\nExample input:\nData Table Configuration\nUser Profile Management\nReal-time Analytics Dashboard\n\nExample output:\n~~~\n[\n { \"lang\": \"zh\_CN\", \"name\": \"中文\", \"text\": \"数据表配置\" },\n { \"lang\": \"en\_US\", \"name\": \"英文\", \"text\": \"Data Table Configuration\" },\n { \"lang\": \"ja\_JP\", \"name\": \"日文\", \"text\": \"データテーブル構成\" },\n { \"lang\": \"ko\_KR\", \"name\": \"韩文\", \"text\": \"데이터 테이블 구성\" },\n { \"lang\": \"fr\_FR\", \"name\": \"法文\", \"text\": \"Configuration du tableau de données\" },\n { \"lang\": \"de\_DE\", \"name\": \"德文\", \"text\": \"Datentabellenkonfiguration\" },\n { \"lang\": \"es\_ES\", \"name\": \"西班牙文\", \"text\": \"Configuración de tabla de datos\" },\n { \"lang\": \"ar\_SA\", \"name\": \"阿拉伯文\", \"text\": \"تكوين جدول البيانات\" },\n { \"lang\": \"pt\_BR\", \"name\": \"葡萄牙文\", \"text\": \"Configuração da tabela de dados\" },\n { \"lang\": \"ru\_RU\", \"name\": \"俄文\", \"text\": \"Конфигурация таблицы данных\" },\n { \"lang\": \"it\_IT\", \"name\": \"意大利文\", \"text\": \"Configurazione tabella dati\" },\n { \"lang\": \"th\_TH\", \"name\": \"泰文\", \"text\": \"การกำหนดค่าตารางข้อมูล\" }\n]\n~~~\n\nMaintain accurate terminology and cultural appropriateness in each language.\n~~~~\n有效的AI提示词应该具体、清晰且包含足够的上下文信息。通过使用结构化的提示词模板，可以获得更准确、更符合需求的AI输出。\n总结\n  AI提示词是现代前端开发的重要工具，掌握有效的提示词技巧可以显著提升开发效率和代码质量。关键要点包括：\n明确目标：清楚描述需要生成的代码功能和特性\n提供上下文：包含技术栈、约束条件、性能要求等信息\n结构化组织：使用清晰的结构化格式提高AI理解能力\n迭代优化：根据AI输出进行调整和优化\n质量检查：始终审查AI生成的代码确保质量和安全性\n  随着AI技术的不断发展，提示词工程将成为前端开发者的核心技能之一。通过不断练习和优化提示词策略，开发者可以更有效地利用AI工具提升工作效率。","showReadNum":779,"sourceDetail":null,"sourceType":99,"status":2,"summary":"AI提示词是与AI工具进行有效沟通的关键，合适的提示词可以显著提升代码生成质量和开发效率。","tagIds":[17554,17607,16461,17205,17393],"title":"常见AI提示词整理——前端开发与代码生成最佳实践","uid":3560095,"updateTime":1773136087,"userSummary":"","userUpdateTime":1773136087,"isNewArticle":false},"authorInfo":{"articleNum":0,"avatarUrl":"https://developer.qcloudimg.com/http-save/10011/8d67ab79c421967e5c5da016ab49a1c9.jpg","company":"","introduce":"pandaoh","isProfessionVerified":0,"nickname":"老猫-Bond","privilege":1,"title":"","uid":3560095},"authorType":{"isBlogMoveAuthor":1,"isCoCreator":0,"isInternalAuthor":0,"isOriginalAuthor":0},"classify":[{"id":3,"name":"前端"}],"columnInfo":{"columnAvatar":"https://developer.qcloudimg.com/http-save/yehe-3560095/b13cc72fec54737cef02ed4d7340c4bf.png","columnDesc":"","columnId":101457,"columnName":"前端大全","createTime":1701757650,"createUid":3560095,"memberNum":1,"showArticleNum":85,"showConcernNum":16},"columnList":[{"columnAvatar":"https://developer.qcloudimg.com/http-save/yehe-3560095/b13cc72fec54737cef02ed4d7340c4bf.png","columnDesc":"","columnId":101457,"columnName":"前端大全","createTime":1701757650,"createUid":3560095,"memberNum":1,"showArticleNum":85,"showConcernNum":16}],"editTime":0,"grayWords":[],"isTencent":false,"longtailTags":[],"publishTime":1773136087,"sourceDetail":{"blogType":2,"blogUrl":"https://a.biugle.cn","channelSource":"biugle","originalTime":"2025-11-29","sourceAuthor":"","sourceLink":"https://a.biugle.cn/ai\_prompt\_collection\_guide/","wechatNickName":"","wechatUserName":""},"tags":[{"categoryId":99,"createTime":"2023/03/14 11:34:59","groupId":0,"groupName":"","tagId":17554,"tagName":"优化"},{"categoryId":99,"createTime":"2023/03/14 11:35:00","groupId":0,"groupName":"","tagId":17607,"tagName":"最佳实践"},{"categoryId":99,"createTime":"2023/03/14 11:34:40","groupId":0,"groupName":"","tagId":16461,"tagName":"text"},{"categoryId":99,"createTime":"2023/03/14 11:34:53","groupId":0,"groupName":"","tagId":17205,"tagName":"测试"},{"categoryId":99,"createTime":"2023/03/14 11:34:57","groupId":0,"groupName":"","tagId":17393,"tagName":"配置"}],"tdk":{"description":"前端开发AI提示词指南：掌握React/Vue组件生成、CSS样式优化、代码重构、性能调优等高效提示词技巧，提升开发效率与代码质量。包含国际化、测试用例、安全编程等专业场景模板，助力开发者精准获取AI生成代码。","keywords":["AI提示词","前端开发","代码生成","React组件"]},"textLink":[{"ext":{"categoryId":1032,"categoryName":"通用技术 - 开发工具","desc":"响应式设计是一种网站设计方法，它可以使网站在不同的设备上（如台式机、笔记本电脑、平板电脑和智能手机）自动适应不同的屏幕尺寸和分辨率，以提供更好的用户体验。响应式设计通常使用流式布局、灵活的图像和媒体查询等技术来实现。这种设计方法可以使网站在不同的设备上看起来一致，并且能够自动适应不同的屏幕尺寸和分辨率，从而提高网站的可用性和可访问性。","kpCount":9,"name":"响应式设计","pCategoryId":1002,"termId":1876},"id":3583,"link":"https://cloud.tencent.com/developer/techpedia/1876","sources":[2],"text":"响应式设计"},{"ext":{"categoryId":1030,"categoryName":"通用技术 - 安全","desc":"安全编程（Secure Programming）是一种编程方法论，旨在通过编写安全可靠的代码来保护计算机系统和数据的安全性。安全编程涵盖了软件设计、开发、测试和维护的整个生命周期，旨在最大程度地降低软件漏洞和安全缺陷的风险","kpCount":11,"name":"安全编程","pCategoryId":1002,"termId":1772},"id":3485,"link":"https://cloud.tencent.com/developer/techpedia/1772","sources":[2],"text":"安全编程"},{"ext":{"categoryId":1029,"categoryName":"通用技术 - 测试","desc":"单元测试是一种软件测试方法，用于测试程序中最小的可测试单元——函数、方法、类等。单元测试的目的是确保每个单元都能独立地正常工作，从而提高整个程序的质量、可靠性和可维护性。单元测试通常由开发人员编写，它们可以在编写代码时进行，也可以在代码提交之前进行，以确保代码的正确性。单元测试通常使用自动化测试工具来执行测试用例，并生成测试报告。","kpCount":11,"name":"单元测试","pCategoryId":1002,"termId":1925},"id":3623,"link":"https://cloud.tencent.com/developer/techpedia/1925","sources":[2],"text":"单元测试"},{"ext":{"categoryId":1018,"categoryName":"通用技术 - 编程语言","desc":"TypeScript是一种开源的编程语言，它是JavaScript的一个超集，由Microsoft开发和维护。TypeScript通过添加静态类型、类、接口和模块等概念，使得JavaScript能够更好地支持大型应用程序的开发和维护。TypeScript的编译器会将TypeScript代码编译成JavaScript代码，使得TypeScript代码可以在任何支持JavaScript的平台上运行。","kpCount":7,"name":"TypeScript","pCategoryId":1002,"termId":2042},"id":3737,"link":"https://cloud.tencent.com/developer/techpedia/2042","sources":[2],"text":"TypeScript"},{"ext":{"categoryId":1023,"categoryName":"通用技术 - 数据结构与算法","desc":"JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，它是基于JavaScript语言的一个子集，可以用于存储和传输数据。JSON格式的数据是一种键值对的结构，用于表示复杂的数据结构，如数组和嵌套的对象。JSON的语法简洁明了，易于阅读和编写，同时也易于解析和生成，因此在Web应用程序中广泛使用。JSON格式的数据可以用于前后端之间的数据交换、存储和传输，并且可以与多种编程语言进行互操作性。","kpCount":18,"name":"JSON","pCategoryId":1002,"termId":1569},"id":3313,"link":"https://cloud.tencent.com/developer/techpedia/1569","sources":[2],"text":"JSON"},{"ext":{"categoryId":1020,"categoryName":"通用技术 - 云计算","desc":"API是Application Programming Interface的英文缩写，指的是应用程序接口。API定义了软件系统中的组件之间的交互方式，允许不同的软件之间进行交互和通信。它是一组规定的约定和协议，用于定义软件中不同模块和组件之间的通信方式。","kpCount":6,"name":"API","pCategoryId":1002,"termId":1539},"id":3297,"link":"https://cloud.tencent.com/developer/techpedia/1539","sources":[2],"text":"API"},{"ext":{"categoryId":1017,"categoryName":"通用技术 - 移动开发","desc":"SDK是指软件开发工具包（Software Development Kit），也称为开发包或者开发工具包。SDK通常是由一个或多个软件开发工具组成的集合，用于帮助开发者创建、测试和部署软件应用程序。","kpCount":14,"name":"SDK","pCategoryId":1002,"termId":1839},"id":3548,"link":"https://cloud.tencent.com/developer/techpedia/1839","sources":[2],"text":"SDK"},{"ext":{"categoryId":1018,"categoryName":"通用技术 - 编程语言","desc":"CSS（层叠样式表）是一种用于描述HTML（超文本标记语言）和XML（可扩展标记语言）等文档外观和样式的语言。它可以控制网页中的字体、颜色、布局、边框、背景等方面的样式。CSS通过将样式与HTML文档分离，使网页的样式和布局更加灵活、可维护和可扩展。CSS可以在网页中内嵌、链接或直接写入HTML标记中。","kpCount":7,"name":"CSS","pCategoryId":1002,"termId":2043},"id":3738,"link":"https://cloud.tencent.com/developer/techpedia/2043","sources":[2],"text":"CSS"},{"ext":{"categoryId":1017,"categoryName":"通用技术 - 移动开发","desc":"UX（User Experience）是指用户在使用产品、服务或系统时所感受到的全部经历和情感反应。UX设计旨在提高用户满意度，增强用户忠诚度，从而提升产品或服务的市场竞争力。UX设计通常包括用户研究、信息架构、交互设计、视觉设计等方面，旨在创造出让用户感觉舒适、易用和具有吸引力的产品或服务。","kpCount":13,"name":"UX","pCategoryId":1002,"termId":1843},"id":3552,"link":"https://cloud.tencent.com/developer/techpedia/1843","sources":[2],"text":"UX"}]},"#url:\"/api/tag/products\",params:#tagIds:@17554,17607,16461,17205,17393,,objectType:1,objectId:2636348,,":[]},"tdk":{"title":"常见AI提示词整理——前端开发与代码生成最佳实践-腾讯云开发者社区-腾讯云","keywords":"AI提示词,前端开发,代码生成,React组件","description":"前端开发AI提示词指南：掌握React/Vue组件生成、CSS样式优化、代码重构、性能调优等高效提示词技巧，提升开发效率与代码质量。包含国际化、测试用例、安全编程等专业场景模板，助力开发者精准获取AI生成代码。"},"meta":{"subject":"其他-空类-优化,其他-空类-最佳实践,其他-空类-text,其他-空类-测试,其他-空类-配置","subjectTime":"2026-03-10 17:48:07","articleSource":"B","magicSource":"N","authorType":"Z","productSlug":"none","authorUID":3560095},"link":{"canonical":"https://cloud.tencent.com/developer/article/2636348"},"cssName":["Article","DraftMaster","Player","Katex"],"rbConfigKeys":["groupQRKeywords"],"pvId":"6YF\_WYicUmFumhno3cbcu","clientIp":"240e:305:7886:c900:59c9:c04:6504:5205","globalAnnounce":{"announceId":0},"rbConfig":{"groupQRKeywords":{"AI":{"keywords":[],"img":"https://qcloudimg.tencent-cloud.cn/raw/89b22f53dc3d4e0516d0a4f74ab01a30.png"}},"versionUpdateTipList":[{"id":1008,"title":"一站式MCP教程库，解锁AI应用新玩法","description":"涵盖代码开发、场景应用、自动测试全流程，助你从零构建专属AI助手","start\_time":"2025/09/08 00:00:00","end\_time":"2025/10/08 23:59:59","url":"https://cloud.tencent.com/developer/special/mcp?from=28419\u0026from\_column=28419"},{"id":1009,"title":"社区富文本\u0026Markdown编辑器全新改版上线，欢迎大家体验!","description":"聚焦“写作效率、视觉美观与运行性能”三方面进行全面升级，为您提供更高效、稳定的创作环境","start\_time":"2025/11/17 00:00:00","end\_time":"2025/11/20 23:59:59","url":"https://cloud.tencent.com/developer/article/write?fromchannel=update\_notice"},{"id":1010,"title":"社区新版编辑器体验调研","description":"诚挚邀请您参与本次调研，分享您的真实使用感受与建议。您的反馈至关重要，感谢您的支持与参与！","start\_time":"2025/12/01 00:00:00","end\_time":"2025/12/05 23:59:59","url":"https://doc.weixin.qq.com/forms/AJEAIQdfAAoAVIAoAZxAL0CN9ODn0Xvaf?page=1"}],"navList":[{"text":"学习","menuList":[{"iconName":"article","title":"文章","desc":"技术干货聚集地","href":"/developer/column?from=19154"},{"iconName":"ask","title":"问答","desc":"技术问题讨论区","href":"/developer/ask?from=19155"},{"iconName":"video","title":"视频","desc":"技术视频记录区","href":"/developer/video?from=19156"},{"iconName":"https://qccommunity.qcloudimg.com/icons/%E6%8A%80%E6%9C%AF%E5%AD%A6%E4%B9%A0.svg","title":"教程","desc":"技术学习实践区","href":"/developer/tutorial/practice"},{"iconName":"learn","title":"学习中心","desc":"一站式学习平台","href":"/developer/learning"},{"iconName":"lab","title":"腾讯云实验室","desc":"体验腾讯云产品功能","href":"/lab/labslist?from=20154\u0026from\_column=20154\u0026channel=c1004\u0026sceneCode=dev"}]},{"text":"活动","menuList":[{"iconName":"living","title":"直播","desc":"技术大咖面对面","href":"/developer/salon?from=19161"},{"iconName":"competition","title":"竞赛","desc":"秀出你的技术影响力","href":"/developer/competition?from=19162"}]},{"text":"专区","menuList":[{"iconName":"https://qccommunity.qcloudimg.com/icons/demo-analyze.svg","title":"腾讯云代码分析专区","desc":"关注每行代码迭代","href":"/developer/zone/tencentcloudcodeanalysis"},{"iconName":"https://qccommunity.qcloudimg.com/icons/ioa.svg","title":"腾讯iOA零信任安全管理系统专区","desc":"腾讯自研自用的办公安全一体化平台","href":"/developer/zone/zerotrustsecuritymanagement"},{"iconName":"https://qccommunity.qcloudimg.com/icons/tm-zone.svg","title":"腾讯云架构师技术同盟交流圈","desc":"架构行家智汇，海量一线案例","href":"/developer/zone/tm"},{"iconName":"https://qcloudimg.tencent-cloud.cn/raw/1deae15bfe2dcdd1036f601852df7dd2.svg","title":"腾讯云数据库专区","desc":"数据智能管理专家","href":"/developer/zone/tencentdb"},{"iconName":"https://qccommunity.qcloudimg.com/icons/cloud\_assistant.svg","title":"腾讯云智能顾问专区","desc":"实现便捷、灵活的一站式云上治理","href":"/developer/zone/tencentcloudsmartadvisor"},{"iconName":"cloudnative","title":"腾讯云原生专区","desc":"助力业务降本增效","href":"/developer/zone/cloudnative?from=19164"},{"iconName":"https://qccommunity.qcloudimg.com/icons/tencenthunyuan.svg","title":"腾讯混元专区","desc":"具备强大的中文创作、逻辑推理、任务执行能力","href":"/developer/zone/tencenthunyuan"},{"iconName":"https://qcloudimg.tencent-cloud.cn/raw/1d60f881ef280ea992e2e4b6490d974b.svg","title":"腾讯云TCE专区","desc":"私有化云解决方案","href":"/developer/zone/tce"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/lighthouse.svg","title":"腾讯云Lighthouse专区","desc":"新一代开箱即用、面向轻量应用场景的云服务器","href":"/developer/zone/lighthouse"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/HAi.svg","title":"腾讯云HAI专区","desc":"提供即插即用的高性能云服务","href":"/developer/zone/hai"},{"iconName":"https://cloudcache.tencent-cloud.com/qcloud/ui/static/static\_source\_business/b3e1b483-be77-4e08-827f-ef0e5cda26cf.svg","title":"腾讯云Edgeone专区","desc":"下一代CDN—EdgeOne，不止加速","href":"/developer/zone/tencentcloudedgeone"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/cos.svg","title":"腾讯云存储专区","desc":"安全稳定的海量分布式存储服务","href":"/developer/zone/cos"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/ai.svg","title":"腾讯云智能专区","desc":"数实融合，云上智能","href":"/developer/zone/ai"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/ipass.svg","title":"腾讯轻联专区 ","desc":"新一代应用与数据集成平台","href":"/developer/zone/ipaas"},{"iconName":"https://qccommunity.qcloudimg.com/image/cloudbase.svg","title":"腾讯云开发专区","desc":"云原生一体化开发平台","href":"/developer/zone/tencentcloudbase"},{"iconName":"https://qccommunity.qcloudimg.com/image/TAPD.svg","title":"TAPD专区","desc":"让协作更敏捷","href":"/developer/zone/tapd"},{"iconName":"https://qccommunity.qcloudimg.com/icons/game.svg","title":"腾讯轻量云游戏服专区","desc":"一键开服，畅快开玩，稳定可靠的游戏服务器","href":"/developer/zone/lightgame"}]},{"text":"圈层","menuList":[{"iconName":"https://qccommunity.qcloudimg.com/community/image/sphereExpert.svg","title":"腾讯云最具价值专家","desc":"汇聚行业顶级技术专家，用科技影响世界","href":"/tvp"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/sphereAlliance.svg","title":"腾讯云架构师技术同盟","desc":"同盟共创，关注每位架构师成长","href":"/developer/program/tm"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/sphereStar.svg","title":"腾讯云创作之星","desc":"做知识摆渡人，共造技术普惠加速度","href":"/developer/program/tci"},{"iconName":"https://qccommunity.qcloudimg.com/community/image/spherePioneer.svg","title":"腾讯云开发者先锋","desc":"聚技术先锋之力，携开发者共拓产品新界","href":"/developer/program/tdp"}]},{"text":"工具","menuList":[{"iconName":"https://qccommunity.qcloudimg.com/icons/ai-assistant.svg","title":"腾讯云代码助手","desc":"辅助编码工具，使研发提效增质","href":"/product/acc?from=22178"},{"iconName":"https://qccommunity.qcloudimg.com/icons/CNB.svg","title":"云原生构建","desc":"帮助开发者以更酷的方式构建软件","href":"/product/cnb?Is=sdk-topnav"},{"iconName":"https://qccommunity.qcloudimg.com/image/TAPD.svg","title":"TAPD 敏捷项目管理","desc":"让协作更敏捷","href":"/product/tapd?Is=sdk-topnav"},{"iconName":"studio","title":"Cloud Studio","desc":"随时随地在线协作开发","href":"https://cloudstudio.net/"},{"iconName":"sdk","title":"SDK中心","desc":"开发者语言与SDK","href":"/document/sdk?from=20154\u0026from\_column=20154"},{"iconName":"api","title":"API中心","desc":"API 助力快捷使用云产品","href":"/document/api?from=20154\u0026from\_column=20154"},{"iconName":"tool","title":"命令行工具","desc":"可快速调用管理云资源","href":"/document/product/440/6176?from=20154\u0026from\_column=20154"}]}],"activity-popup":{"mImgUrl":"https://qccommunity.qcloudimg.com/mp/images/11-11mobile.jpg","imgUrl":"https://qccommunity.qcloudimg.com/mp/images/11-11pc.jpg","beginTime":"2024/10/24 00:00:00","endTime":"2024/10/31 23:59:59"},"header-advertisement":{"imageUrl":"https://qccommunity.qcloudimg.com/image/2024-11-01-18-15.png","link":"https://cloud.tencent.com/act/pro/double11-2024?from=22374\u0026from\_column=22374#miaosha"}},"isBot":false,"session":{"isLogined":false,"isQCloudLogined":false,"isQCommunityLogined":false,"isDifferentUin":false,"editMode":"rich"}}},"page":"/article/[articleId]","query":{"articleId":"2636348"},"buildId":"y23d\_CXebUuPHP\_r4lWtf","assetPrefix":"https://qccommunity.qcloudimg.com/community","isFallback":false,"gssp":true,"appGip":true,"scriptLoader":[]}