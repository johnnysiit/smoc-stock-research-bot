#Author: Juanxi Xue
#This is the main introduce page of the program, run this py file to start the program
import shutil


def get_tickers():
    ticker = str(input("请输入股票代码 Please type in the symbol of the stock: "))
    output_mode = int(input("\n1.Excel\n2.Console Print 终端直接输出\n请选择输出方式 Please select the output mode: "))
    return ticker, output_mode

print("\n==========================================\n|| Welcome to SMOC Data Process System ||\n==========================================\n")
print("请选择运行程序 Pleae select the program you want to run:")
print("1. Equity Statistic Data (Ratio/Multiplies Comparison)\n2. Financial Statement Analysis\n3. Volatility Strategy (For Spread Option Use)\n4. Modeling tools (DDM, Multipliers, FCFE, Valuation)\n5. Bond Calculator\n6. CAPM Functions (SML, CML, Sharpe, M^2, Treynor\n7. Exit")
program_run = input("Please enter a number: ")

if program_run == "1":
    import Stock_Comparison.sct as sct
    sct.main()
elif program_run == "2":
    import Statement_Grading.mgs as mgs
    import Statement_Grading.fin_stmt_excel as fse
    mode = input("\nPlease select the mode you want to run: \n1. Multi-stock Metrix Ranking\n2. Single Stock Metrix Detail Analysis\n3. Get an Excel financial statement only\nPlease enter a number: ")
    if mode == "3":
        ticker,output_mode = get_tickers()
        print("\n请稍等，总时长可能会超过2分钟 Please wait... The whole process might take over 2 minutes....\n")
        fse.main(ticker,output_mode)
    elif mode == "2":
        print("\nAttention: This system cannot apply on the data of financial industry.\n请注意：该系统不适用于金融行业的财报数据\n")
        ticker,output_mode = get_tickers()
        runmode = int(input("\n1.Normal Mode\n2.Fast Mode (Skip Preferred Stock Dividend)\n请选择运行模式 Please select the run mode: "))
        print("\nNow analyzing the data\n开始分析数据\n")
        mgs.main(ticker,output_mode,runmode)
        print("\nFRAPS Finished Running!\nFARPS完成运行，感谢支持!\n")
    elif mode == "1":
        print ("This function is not ready yet. If you want to try this function, run ranking.py instead.")
elif program_run == "3":
    import Volatility_Strategy.main as vs
    notice = input("\nPlease enter your stock list on the file /Volatility_Strategy/ticker.txt\nWhen you ready, press enter to continue")
    vs.main()
elif program_run == "4":
    print("This function is not ready yet. If you want to try this function, run modeling.py instead.")
elif program_run == "5":
    print("This function is not ready yet. If you want to try this function, run bond.py instead.")
elif program_run == "6":
    import CAPM.main as capm
    ticker = input("Please enter the ticker of the stock: ")
    capm.main(ticker)
elif program_run == "7":
    print("\nThank you for using this program!\n感谢使用！\n")
else:
    print ("\nPlease enter a valid number!\n请输入有效数字！\n")
    
try: 
    shutil.rmtree("__pycache__")
    shutil.rmtree("./CAPM/__pycache__")
    shutil.rmtree("./Statement_Grading/__pycache__")
    shutil.rmtree("./Stock_Comparison/__pycache__")
    shutil.rmtree("./Volatility_Strategy/__pycache__")
    print("====Exit====Code:1")
except:
    print ("====Exit====Code:2")
