import excel_maker as em
import fin_stmt_excel as fse

print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
print("\nAttention: This system cannot apply on the data of financial industry.\n请注意：该系统不适用于金融行业的财报数据\n")
ticker = str(input("请输入股票代码 Please type in the symbol of the stock: "))
output_mode = int(input("\n1.Excel\n2.Console Print 终端直接输出\n请选择输出方式 Please select the output mode: "))
print("\n请稍等，总时长可能会超过2分钟 Please wait... The whole process might take over 2 minutes....\n")
fse.main(ticker,output_mode)
print("\nNow analyzing the data\n开始分析数据\n")
em.main(ticker,output_mode)
