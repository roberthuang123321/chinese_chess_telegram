from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import random
import time

def initial_board():


    black = ['將', '士', '士', '象', '象', '車', '車', '馬', '馬', '砲', '砲', '卒', '卒', '卒', '卒', '卒']
    red = ['帥', '仕', '仕', '相', '相', '俥', '俥', '傌', '傌', '炮', '炮', '兵', '兵', '兵', '兵', '兵']
    board = black + red
    shuffled_board = random.sample(board, len(board))
    new_board = [shuffled_board[i:i + 4] for i in range(0, len(shuffled_board), 4)]
    return new_board

async def start(update, context):
    context.user_data['click'] =0
    context.user_data['turn'] = 0
    hidden_board = initial_board()
    context.user_data['hidden_board'] = hidden_board
    context.user_data['board']  = [['○' for _ in range(4)] for _ in range(8)]
    keyboard = [[InlineKeyboardButton('○', callback_data=f"{row},{col}") for col in range(4)] for row in range(8)]
    await update.message.reply_text('由你先下', reply_markup=InlineKeyboardMarkup(keyboard))

def make_move(board, hidden_board, row, col, row_1, col_1, context):
    # 將棋子從起始位置移動到结束位置
    board[row_1][col_1] = board[row][col]
    hidden_board[row_1][col_1] = hidden_board[row][col]
    board[row][col] = ' '
    hidden_board[row][col] = ' '
def count_pieces_in_path(board, initial_row, initial_col, final_row, final_col):
    # 計算路徑上的棋子數量（不包括起點和终點）
    count = 0
    if initial_row == final_row:  # 在同一行
         for col in range(min(initial_col, final_col) + 1, max(initial_col, final_col)):
            if board[initial_row][col] != ' ':
                count += 1
    if initial_col == final_col:  # 在同一列
        for row in range(min(initial_row, final_row) + 1, max(initial_row, final_row)):
            if board[row][initial_col] != ' ':
                count += 1
    return count
def can_eat(start_chess, end_chess):
    black = ['將', '士', '士', '象', '象', '車', '車', '馬', '馬', '砲', '砲', '卒', '卒', '卒', '卒', '卒']
    red = ['帥', '仕', '仕', '相', '相', '俥', '俥', '傌', '傌', '炮', '炮', '兵', '兵', '兵', '兵', '兵']
    rank = {'○':10, ' ': 0, '將': 7, '帥': 7, '士': 6, '仕': 6, '象': 5, '相': 5, '車': 4, '俥': 4, '馬': 3, '傌': 3, '砲': 2, '炮': 2,
            '卒': 1, '兵': 1}

    start_rank = rank.get(start_chess)
    end_rank = rank.get(end_chess)
    print(start_rank)
    print(end_rank)
    if start_chess in black and  end_chess in red :
        if start_rank ==1 and end_rank==7:
            return True
        if start_rank ==7 and end_rank == 1:
            return False
        if start_rank > end_rank :
            return True
        if start_rank == end_rank :
            return True
        else:
            return False
    if start_chess in red and  end_chess in black :
        if start_rank == 1 and end_rank == 7:
            return True
        if start_rank ==7 and end_rank == 1:
            return False
        if start_rank > end_rank:
            return True
        if start_rank == end_rank:
            return True
        else:
            return False
    if end_chess==' ' :
        return True
    else:
        # 如果其中一個棋子不在 rank 字典中，可以根據你的需求返回 True 或 False
        return False

def legal_move(board, hidden_board, initial_row, initial_col, final_row, final_col):
    start_chess = board[initial_row][initial_col]
    end_chess = board[final_row][final_col]
   # 考慮'砲'/'炮'的情況
    if start_chess in ['砲', '炮']:
        # 炮在不吃子時只能前進一格
        if end_chess == ' ':
            if (-1 <= final_row - initial_row <= 1 and final_col - initial_col == 0):
                return True
            if (final_row - initial_row == 0 and -1 <= final_col - initial_col <= 1):
                return True

        # 炮吃子時要相隔一枚棋子
        if start_chess[0] != end_chess[0]: # 吃子時與炮顏色不同
            if board[final_row][final_col] != "○":
                if count_pieces_in_path(board, initial_row, initial_col, final_row, final_col) == 1:
                    return True
        return False

    else:
        if -1 <= final_row - initial_row <= 1 and final_col - initial_col == 0:
            if can_eat(start_chess, end_chess) == True:
                return True
        if final_row - initial_row == 0 and -1 <= final_col - initial_col <= 1:
            if can_eat (start_chess, end_chess) == True:
                return True
        else :
            return False
# 在你的 bot_action 函數中...
async def bot_action(context, chat_id, message_id, board, hidden_board):
    # 這只是一個簡單的例子，實際情況中你可能需要一個更智能的機器人行為
    # 這個例子中，機器人隨機選擇是翻開一個位置還是移動一枚棋子
    time.sleep(1)
    black = ['將', '士', '士', '象', '象', '車', '車', '馬', '馬', '砲', '砲', '卒', '卒', '卒', '卒', '卒']
    red = ['帥', '仕', '仕', '相', '相', '俥', '俥', '傌', '傌', '炮', '炮', '兵', '兵', '兵', '兵', '兵']
    bot_color = context.user_data.get('bot_color')
    if bot_color == "black" :
        bot_pieces = [(r, c) for r in range(8) for c in range(4) if hidden_board[r][c] in black and board[r][c] != '○']
    else:
        bot_pieces = [(r, c) for r in range(8) for c in range(4) if hidden_board[r][c] in red and board[r][c] != '○']

    print(bot_pieces)
    # 找到還沒被翻開的位置
    empty_positions = [(r, c) for r in range(8) for c in range(4) if board[r][c] == '○']
    while True :

            # 隨機選擇是翻開一個位置還是移動一枚棋子
            random_choice_1 = random.choice(['reveal', 'move'])
            if context.user_data['turn'] ==1 :
                random_position = random.choice(empty_positions)
                row, col = random_position
                board[row][col] = hidden_board[row][col]
                break
            if bot_pieces == [] and empty_positions!= []:
                random_position = random.choice(empty_positions)
                row, col = random_position
                board[row][col] = hidden_board[row][col]
                break
            if random_choice_1 == 'reveal' and empty_positions!= []:
                # 隨機選擇一個位置翻開
                random_position = random.choice(empty_positions)
                row, col = random_position
                board[row][col] = hidden_board[row][col]
                break
            if random_choice_1 == 'move' :
                # 隨機選擇一枚棋子移動
                random_piece = random.choice(bot_pieces)
                row, col = random_piece
                legal_moves = [(r, c) for r in range(8) for c in range(4) if legal_move(board, hidden_board, row, col, r, c)]
                if legal_moves:
                    random_move = random.choice(legal_moves)
                    row_2, col_2 = random_move
                    make_move(board, hidden_board, row, col, row_2, col_2, context)
                    break
                else :
                    continue
            if  empty_positions == []:
                # 隨機選擇一枚棋子移動
                random_piece = random.choice(bot_pieces)
                row, col = random_piece
                legal_moves = [(r, c) for r in range(8) for c in range(4) if
                               legal_move(board, hidden_board, row, col, r, c)]
                if legal_moves:
                    random_move = random.choice(legal_moves)
                    row_2, col_2 = random_move
                    make_move(board, hidden_board, row, col, row_2, col_2, context)
                    break
                else:
                    continue


async def check_game_over(context, hidden_board, board):
    black = ['將', '士', '士', '象', '象', '車', '車', '馬', '馬', '砲', '砲', '卒', '卒', '卒', '卒', '卒']
    red = ['帥', '仕', '仕', '相', '相', '俥', '俥', '傌', '傌', '炮', '炮', '兵', '兵', '兵', '兵', '兵']
    chat_id = context.user_data.get('chat_id')

    black_pieces = [(r, c) for r in range(8) for c in range(4) if hidden_board[r][c] in black and board[r][c] != '○']
    red_pieces = [(r, c) for r in range(8) for c in range(4) if hidden_board[r][c] in red and board[r][c] != '○']
    if black_pieces ==[] :
        await context.bot.send_message(chat_id=chat_id, text="紅方獲勝！")
        return True  # 遊戲結束
    if red_pieces == []:
        await context.bot.send_message(chat_id=chat_id, text="黑方獲勝！")
        return True  # 遊戲結束

    return False  # 遊戲未結束




async def handler(update, context):
    black = ['將', '士', '士', '象', '象', '車', '車', '馬', '馬', '砲', '砲', '卒', '卒', '卒', '卒', '卒']
    red = ['帥', '仕', '仕', '相', '相', '俥', '俥', '傌', '傌', '炮', '炮', '兵', '兵', '兵', '兵', '兵']
    context.user_data['turn'] = context.user_data['turn']+1
    context.user_data['click'] = context.user_data['click'] +1
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    context.user_data['chat_id'] = chat_id
    board = context.user_data.get('board')
    hidden_board = context.user_data.get('hidden_board')
    global row ,col

    if context.user_data['turn'] ==1 : #第一回合判斷顏色
        row, col = map(int, query.data.split(','))
        board[row][col] = hidden_board[row][col]
        if board[row][col] in black:
            player_color = 'black'
        else:
            player_color = 'red'
        print(player_color)
        bot_color = 'red' if player_color == 'black' else 'black'
        context.user_data['player_color'] = player_color
        context.user_data['bot_color'] = bot_color
        # 更新棋盤顯示
        keyboard = [[InlineKeyboardButton(board[r][c], callback_data=f"{r},{c}") for c in range(4)] for r in
                    range(8)]
        await context.bot.edit_message_text('棋盤:', reply_markup=InlineKeyboardMarkup(keyboard),
                                            chat_id=query.message.chat_id,
                                            message_id=query.message.message_id)

        await bot_action(context, query.message.chat_id, query.message.message_id, board, hidden_board)
        context.user_data['click']=0
        # 更新棋盤顯示
        keyboard = [[InlineKeyboardButton(board[r][c], callback_data=f"{r},{c}") for c in range(4)] for r in
                    range(8)]
        await context.bot.edit_message_text('棋盤:', reply_markup=InlineKeyboardMarkup(keyboard),
                                            chat_id=query.message.chat_id,
                                            message_id=query.message.message_id)
        await context.bot.send_message(chat_id=query.message.chat_id,
                                       text=f"你是 {'黑棋' if player_color == 'black' else '紅棋'}，Bot 是 {'黑棋' if bot_color == 'black' else '紅棋'}。")
        return


    if context.user_data['click'] == 1:
        row, col = map(int, query.data.split(','))
        if board[row][col] == '○':
            # 翻棋
            board[row][col] = hidden_board[row][col]
            # 更新棋盤顯示
            keyboard = [[InlineKeyboardButton(board[r][c], callback_data=f"{r},{c}") for c in range(4)] for r in
                        range(8)]
            await context.bot.edit_message_text('棋盤:', reply_markup=InlineKeyboardMarkup(keyboard),
                                                chat_id=query.message.chat_id,
                                                message_id=query.message.message_id)
            # 執行 Bot 的回合
            await bot_action(context, query.message.chat_id, query.message.message_id, board, hidden_board)
            # 更新棋盤顯示
            keyboard = [[InlineKeyboardButton(board[r][c], callback_data=f"{r},{c}") for c in range(4)] for r in
                        range(8)]
            await context.bot.edit_message_text('棋盤', reply_markup=InlineKeyboardMarkup(keyboard),
                                                chat_id=query.message.chat_id,
                                                message_id=query.message.message_id)
            context.user_data['click'] = 0
            return

    if context.user_data['click'] == 2:
        row_2, col_2 = map(int, query.data.split(','))
        if legal_move(board, hidden_board, row, col, row_2, col_2) == True:
            make_move(board, hidden_board, row, col, row_2, col_2, context)
            context.user_data['click'] = 0
            # 更新棋盤顯示
            keyboard = [[InlineKeyboardButton(board[r][c], callback_data=f"{r},{c}") for c in range(4)] for r in
                        range(8)]
            await context.bot.edit_message_text('棋盤:', reply_markup=InlineKeyboardMarkup(keyboard),
                                                chat_id=query.message.chat_id,
                                                message_id=query.message.message_id)
            await check_game_over(context, hidden_board, board)
            await bot_action(context, query.message.chat_id, query.message.message_id, board, hidden_board)
            # 更新棋盤顯示
            keyboard = [[InlineKeyboardButton(board[r][c], callback_data=f"{r},{c}") for c in range(4)] for r in
                        range(8)]
            await context.bot.edit_message_text('棋盤', reply_markup=InlineKeyboardMarkup(keyboard),
                                                chat_id=query.message.chat_id,
                                                message_id=query.message.message_id)



            return

        else :
            await context.bot.send_message(chat_id=query.message.chat_id, text="非法移動，請重新選擇棋子")
            context.user_data['click'] = 0
            return







async def echo(update, context):
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6617401443:AAHHeiwEg3SgKETYgLWmV-AHGO-PT7OLhlU").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(CallbackQueryHandler(handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
