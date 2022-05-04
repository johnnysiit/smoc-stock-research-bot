import excel_maker as em
import fin_stmt_excel as fse
import sct

def get_tickers():
    ticker = str(input("请输入股票代码 Please type in the symbol of the stock: "))
    output_mode = int(input("\n1.Excel\n2.Console Print 终端直接输出\n请选择输出方式 Please select the output mode: "))
    return ticker, output_mode

print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
print("请选择运行程序 Pleae select the program you want to run:")
print("1. Stock Comparison Tool\n2. Financial Statement\n3. SMOC Matrix Grading System")
program_run = input("Please enter a number:")
if program_run == "1":
    sct.main()
elif program_run == "2":
    ticker,output_mode = get_tickers()
    print("\n请稍等，总时长可能会超过2分钟 Please wait... The whole process might take over 2 minutes....\n")
    fse.main(ticker,output_mode)
elif program_run == "3":
    print("\nAttention: This system cannot apply on the data of financial industry.\n请注意：该系统不适用于金融行业的财报数据\n")
    ticker,output_mode = get_tickers()
    runmode = int(input("\n1.Normal Mode\n2.Fast Mode (Skip Preferred Stock Dividend)\n请选择运行模式 Please select the run mode: "))
    print("\nNow analyzing the data\n开始分析数据\n")
    em.main(ticker,output_mode,runmode)
    print("\nFRAPS Finished Running!\nFARPS完成运行，感谢支持!\n")
else:
    print ("\nPlease enter a valid number!\n请输入有效数字！\n")