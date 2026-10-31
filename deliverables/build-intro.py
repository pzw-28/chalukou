from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

root = Path(__file__).parent.parent
out = root / 'deliverables' / '岔路口_预指导介绍.docx'
doc = Document()
section = doc.sections[0]
section.top_margin = Cm(1.45)
section.bottom_margin = Cm(1.35)
section.left_margin = Cm(1.65)
section.right_margin = Cm(1.65)

styles = doc.styles
styles['Normal'].font.name = 'Microsoft YaHei'
styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
styles['Normal'].font.size = Pt(9.5)
styles['Normal'].paragraph_format.space_after = Pt(4)
styles['Normal'].paragraph_format.line_spacing = 1.08
for name, size, color in [('Title', 24, '17365D'), ('Heading 1', 15, '17365D'), ('Heading 2', 11.5, '2457D6')]:
    styles[name].font.name = 'Microsoft YaHei'
    styles[name]._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    styles[name].font.size = Pt(size)
    styles[name].font.color.rgb = RGBColor.from_string(color)
    styles[name].font.bold = True
    styles[name].paragraph_format.space_before = Pt(5)
    styles[name].paragraph_format.space_after = Pt(5)


def heading(text, level=1):
    return doc.add_heading(text, level=level)


def para(text, bold_prefix=None):
    p = doc.add_paragraph()
    if bold_prefix and text.startswith(bold_prefix):
        p.add_run(bold_prefix).bold = True
        p.add_run(text[len(bold_prefix):])
    else:
        p.add_run(text)
    return p


def bullets(items):
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.add_run(item)


def numbered(items):
    for item in items:
        p = doc.add_paragraph(style='List Number')
        p.paragraph_format.space_after = Pt(2)
        p.add_run(item)


def image(path, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Cm(15.8))
    cap = doc.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in cap.runs:
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(90, 100, 115)


title = doc.add_paragraph(style='Title')
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.add_run('岔路口')
subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('可核验的考研、就业、考公选择沙盘｜预指导作品介绍')
run.bold = True
run.font.size = Pt(12)
run.font.color.rgb = RGBColor(36, 87, 214)
para('版本：预指导单文件版｜赛道：AI 创新应用挑战赛 Vibe Coding｜公开仓库：https://github.com/pzw-28/chalukou')

heading('一、痛点与用户')
para('大三学生在选择考研、就业或考公时，面对的是分散且难以核验的信息。以国考为例，学生需要在近万行职位条件中判断“我到底能报几个岗”，通用 AI 又可能直接给出没有原表依据的数字。项目首先服务这类需要核对资格、又希望理解条件变化影响的学生。')

heading('二、解决方案与使用方式')
para('岔路口的完整规划是考研、就业、考公三条路。预指导版不铺三张空页面，而是先把考公做成最小闭环：官方数据导入→个人画像→三态筛选→原表溯源→地点差分。')
numbered([
    '用新版 Edge 或 Chrome 双击 index.html，首次打开需联网加载 SheetJS。',
    '选择国家公务员局发布的 2027 国考招考简章 .xls，文件只在浏览器本地解析。',
    '输入专业、学历、学位、政治面貌、届别、基层年限和可接受地点，程序自动重算。',
    '点击三态数字查看职位，点击职位查看 sheet、Excel 行号和 27 列原始字段；清空再选择地点，查看变化量和新增职位。'
])
para('当前范围：只完成考公闭环，不声称考研、就业、AI 讲解员、数字合同、回放或成功率预测已经实现。')

heading('三、真实数据底座')
bullets([
    '国家公务员局 2027 年度考录专题原始 .xls；四个数据 sheet 共 19,426 条职位，空白 Sheet1 自动跳过。',
    '第 2 行表头、第 3 行首条职位；保留文件名、sheet、真实 Excel 行号、全部 27 列和 SHA256。',
    '唯一标识使用“数据版本＋sheet＋Excel 行号”，不因职位代码重复而覆盖职位。'
])

doc.add_page_break()
heading('四、核心原则与创新点')
bullets([
    '资格三态：符合、不符、待确认。任一明确不符才不符；存在未知就待确认；全部已核实满足才符合，宁可待确认也不乱放行。',
    '逐数可核验：页面数字由程序从官方表计算，每个职位都能回到原表物理行和原始字段。',
    '单条件差分：基线绑定数据版本和全部非地点画像，只改地点才计算变化量与新增集合，避免错误归因。',
    '保守边界：专业按学历阶段匹配，学历区分“仅限／或／及以上”；一般应届身份、服务基层身份和未解释备注不被擅自放行。'
])

heading('五、关键技术与 AI 测试技术落地')
para('工程实现：单个 index.html、原生 JavaScript、SheetJS CDN，无后端、无数据库、无需 API Key。AI 不直接参与资格计算。')
bullets([
    '双工具读取：Kimi Code 使用 SheetJS，GPT 使用 OleDb，独立核对 sheet、表头、职位数和关键反例。',
    '真实固定用例：第 58 行验证真实符合，第 67 行验证跨学历阶段不得放行，第 76 行验证仅限硕士拒绝博士，第 128、16993、421 行验证应届与身份待确认。',
    '真实浏览器验收：实际文件输入、职位点击、地点切换和换版本重新导入；结果为符合 1、待确认 12、不符 19,413，地点差分 +1。',
    '独立审查：GPT 两轮指出备注兜底、届别、基线失效和缺少真实正例等阻断项，修订后复审通过。'
])
image(root / 'evidence' / 'screenshots' / '001-main.png', '图 1｜真实官方表导入、三态结果及地点 +1（1920×1080 实际浏览器截图）')

doc.add_page_break()
heading('六、AI 协作过程与工作流')
bullets([
    '先提案再执行：每个功能有 proposal、tasks 和验收标准，按小步提交，禁止一次性生成整个项目。',
    '作者与审查者分离：Kimi Code 实现，GPT 独立读取和审查，用户决定采纳与范围。',
    '每轮留痕：prompt-log 保存用户提问、AI 建议、人的引导、真实失败与验证；公开 GitHub 保留细粒度提交。',
    '排错按证据：复现→根因→证据→修改→验证，不删测试、不改数据迎合结果。'
])
para('真实返工示例：第 58 行预期符合却显示不符。逐项检查发现只有学历误判，根因是“及以上”有 3 个字符，代码却按 4 个字符截取，导致“本科及以上”反把本科排除。只修改截取长度后，同一真实职位由红转绿，完整记录见 prompt-log/P-004.md。')
image(root / 'evidence' / 'screenshots' / '001-detail.png', '图 2｜中央党群机关 Excel 第 58 行、逐项条件与 27 列原表字段')

heading('七、后续三轮迭代计划')
numbered([
    '第二轮：完善专业目录候选、人工金标和完整六项资格判定，迁移 Next.js + TypeScript。',
    '第三轮：加入“差一步”单条件差分、事实卡和受约束 AI 讲解；数字仍只由程序计算。',
    '收尾：补充真实回放、用户试用、技术文档和正式赛 5–8 分钟视频；预指导 2–3 分钟视频不冒充正式赛要求。'
])

heading('八、原创与边界声明')
para('本项目此前未发表、未获奖，不是基于其他项目优化；应用代码按真实需求从头实现。工作流仅借鉴公开方法并注明来源，没有复制参考项目业务代码。没有使用合成数据冒充官方数据。最终资格以招录机关审核为准。视频使用本机 AI 合成普通话配音。')

out.parent.mkdir(parents=True, exist_ok=True)
doc.save(out)
print(out)
