import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Импорты наших модулей
from main import BettingSystem
from bankroll_manager import BettingStrategy
from config import Config

# Настройка страницы
st.set_page_config(
    page_title="🎯 AI Sports Betting System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация состояния
if 'betting_system' not in st.session_state:
    st.session_state.betting_system = None

if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

def init_system():
    """Инициализация системы"""
    if st.session_state.betting_system is None:
        with st.spinner("Инициализация системы..."):
            st.session_state.betting_system = BettingSystem(
                bankroll=Config.INITIAL_BANKROLL,
                strategy=BettingStrategy.MARTINGALE
            )

def main():
    st.title("🎯 Персональная система спортивных ставок с ИИ")
    
    # Боковая панель
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Выбор стратегии
        strategy_options = {
            "Мартингейл (удвоение)": BettingStrategy.MARTINGALE,
            "Фибоначчи": BettingStrategy.FIBONACCI,
            "Фиксированная ставка": BettingStrategy.FLAT,
            "Критерий Келли": BettingStrategy.KELLY,
            "Д'Аламбер": BettingStrategy.DALEMBERT
        }
        
        selected_strategy = st.selectbox(
            "Стратегия управления банкроллом:",
            list(strategy_options.keys())
        )
        
        # Банкролл
        initial_bankroll = st.number_input(
            "Начальный банкролл (руб):",
            min_value=1000,
            max_value=1000000,
            value=Config.INITIAL_BANKROLL,
            step=1000
        )
        
        if st.button("🚀 Инициализировать систему"):
            st.session_state.betting_system = BettingSystem(
                bankroll=initial_bankroll,
                strategy=strategy_options[selected_strategy]
            )
            st.success("Система инициализирована!")
    
    # Основной контент
    tabs = st.tabs(["📊 Дашборд", "🔍 Анализ матчей", "💰 Управление ставками", "📈 Статистика"])
    
    # Инициализируем систему если не инициализирована
    init_system()
    
    with tabs[0]:  # Дашборд
        show_dashboard()
    
    with tabs[1]:  # Анализ матчей
        show_match_analysis()
    
    with tabs[2]:  # Управление ставками
        show_bet_management()
    
    with tabs[3]:  # Статистика
        show_statistics()

def show_dashboard():
    """Главный дашборд"""
    st.header("📊 Дашборд")
    
    if st.session_state.betting_system is None:
        st.warning("Сначала инициализируйте систему в боковой панели")
        return
    
    # Получаем статистику
    stats = st.session_state.betting_system.get_statistics()
    bankroll_stats = stats.get('bankroll_statistics', {})
    
    # Метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Текущий банкролл",
            f"{bankroll_stats.get('current_bankroll', 0):,.0f} ₽",
            delta=f"{bankroll_stats.get('bankroll_change', 0):,.0f} ₽"
        )
    
    with col2:
        st.metric(
            "📊 Процент выигрышей",
            f"{bankroll_stats.get('win_rate', 0):.1f}%"
        )
    
    with col3:
        st.metric(
            "💹 ROI",
            f"{bankroll_stats.get('roi', 0):.1f}%"
        )
    
    with col4:
        st.metric(
            "🎯 Всего ставок",
            bankroll_stats.get('total_bets', 0)
        )
    
    # График банкролла
    if bankroll_stats.get('total_bets', 0) > 0:
        st.subheader("📈 Динамика банкролла")
        
        # Создаем демо данные для графика
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        bankroll_history = [
            Config.INITIAL_BANKROLL + (i * 100) + (i % 5 - 2) * 500 
            for i in range(30)
        ]
        
        fig = px.line(
            x=dates,
            y=bankroll_history,
            title="Изменение банкролла за последние 30 дней"
        )
        fig.update_layout(
            xaxis_title="Дата",
            yaxis_title="Банкролл (₽)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Быстрый анализ матчей на сегодня
    st.subheader("🔍 Матчи на сегодня")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⚽ Анализировать футбол"):
            with st.spinner("Анализируем футбольные матчи..."):
                matches = st.session_state.betting_system.analyze_all_today_matches('football')
                st.session_state.current_analysis = matches
                if matches:
                    st.success(f"Найдено {len(matches)} матчей")
                else:
                    st.info("Матчей на сегодня не найдено")
    
    with col2:
        if st.button("🎮 Анализировать киберспорт"):
            with st.spinner("Анализируем киберспорт..."):
                matches = st.session_state.betting_system.analyze_all_today_matches('esports')
                st.session_state.current_analysis = matches
                if matches:
                    st.success(f"Найдено {len(matches)} матчей")
                else:
                    st.info("Матчей на сегодня не найдено")
    
    # Показываем результаты анализа
    if st.session_state.current_analysis:
        show_matches_preview(st.session_state.current_analysis)

def show_matches_preview(matches):
    """Предварительный просмотр матчей"""
    st.subheader("🎯 Рекомендации по ставкам")
    
    for i, match_data in enumerate(matches[:5]):  # Показываем топ-5
        match = match_data['match']
        recommendation = match_data['recommendation']
        
        with st.expander(f"{match.get('home_team', 'Team A')} vs {match.get('away_team', 'Team B')}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Рекомендация:**", recommendation['action'])
                if recommendation['action'] == 'bet':
                    st.write("**Исход:**", recommendation['outcome'])
                    st.write("**Размер ставки:**", f"{recommendation['bet_size']:.0f} ₽")
            
            with col2:
                if recommendation['action'] == 'bet':
                    st.write("**Коэффициент:**", f"{recommendation['odds']:.2f}")
                    st.write("**Уверенность:**", f"{recommendation['confidence']:.1%}")
                    st.write("**Ожидаемая прибыль:**", f"{recommendation['expected_value']:.3f}")
            
            with col3:
                if recommendation['action'] == 'bet':
                    st.success("✅ Рекомендуется")
                    if st.button(f"Сделать ставку #{i}", key=f"bet_{i}"):
                        # Выполняем ставку
                        result = st.session_state.betting_system.execute_bet(
                            match_data['analysis'], 
                            recommendation
                        )
                        if result['status'] == 'placed':
                            st.success("Ставка размещена!")
                        else:
                            st.warning("Ставка пропущена")
                else:
                    st.info("⏭️ Пропустить")

def show_match_analysis():
    """Детальный анализ матчей"""
    st.header("🔍 Анализ матчей")
    
    if st.session_state.betting_system is None:
        st.warning("Сначала инициализируйте систему")
        return
    
    # Выбор вида спорта
    sport = st.selectbox("Выберите вид спорта:", ["football", "esports"])
    
    # Получаем список матчей
    matches = st.session_state.betting_system.get_today_matches(sport)
    
    if matches:
        # Выбор матча для анализа
        match_options = [
            f"{m.get('home_team', m.get('team1', 'Team A'))} vs {m.get('away_team', m.get('team2', 'Team B'))}"
            for m in matches
        ]
        
        selected_match_idx = st.selectbox(
            "Выберите матч для анализа:",
            range(len(match_options)),
            format_func=lambda x: match_options[x]
        )
        
        selected_match = matches[selected_match_idx]
        
        if st.button("🔍 Анализировать матч"):
            with st.spinner("Анализируем матч..."):
                analysis = st.session_state.betting_system.analyze_match(
                    selected_match['id'], sport
                )
                
                if analysis:
                    show_detailed_analysis(analysis)
                else:
                    st.error("Ошибка при анализе матча")
    else:
        st.info("Матчей на сегодня не найдено")

def show_detailed_analysis(analysis):
    """Показывает детальный анализ матча"""
    st.subheader("📊 Детальный анализ")
    
    match_info = analysis['match_data']['match_info']
    prediction = analysis['prediction']
    bet_analysis = analysis['bet_analysis']
    
    # Основная информация о матче
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Матч:**")
        home_team = match_info.get('home_team', match_info.get('team1', 'Team A'))
        away_team = match_info.get('away_team', match_info.get('team2', 'Team B'))
        st.write(f"{home_team} vs {away_team}")
        st.write("**Дата:**", match_info.get('date', 'N/A'))
        st.write("**Турнир:**", match_info.get('competition', match_info.get('tournament', 'N/A')))
    
    with col2:
        st.write("**Предсказание ИИ:**")
        st.write("**Исход:**", prediction['prediction'])
        st.write("**Уверенность:**", f"{prediction['confidence']:.1%}")
        
        # Вероятности
        st.write("**Вероятности:**")
        for outcome, prob in prediction['probabilities'].items():
            st.write(f"- {outcome}: {prob:.1%}")
    
    # Коэффициенты и ценность ставок
    st.subheader("💰 Анализ ценности ставок")
    
    odds = analysis['match_data']['odds'].get('average_odds', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Коэффициенты:**")
        for outcome, odd in odds.items():
            st.write(f"- {outcome}: {odd:.2f}")
    
    with col2:
        st.write("**Рекомендация:**")
        st.write("**Действие:**", bet_analysis['recommended_action'])
        st.write("**Уровень уверенности:**", bet_analysis['confidence_level'])
        if bet_analysis['recommended_action'] == 'bet':
            st.write("**Исход:**", bet_analysis['recommended_outcome'])
            st.write("**Коэффициент:**", f"{bet_analysis['recommended_odds']:.2f}")
    
    with col3:
        if bet_analysis['value_bets']:
            st.write("**Ценные ставки:**")
            for bet in bet_analysis['value_bets']:
                st.write(f"- {bet['outcome']}: EV={bet['expected_value']:.3f}")
        else:
            st.write("**Ценных ставок не найдено**")
    
    # Статистика команд
    st.subheader("📈 Статистика команд")
    
    home_stats = analysis['match_data']['home_stats']
    away_stats = analysis['match_data']['away_stats']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**{home_team}**")
        st.write(f"Голы забито: {home_stats.get('goals_scored', 0)}")
        st.write(f"Голы пропущено: {home_stats.get('goals_conceded', 0)}")
        st.write(f"Форма: {' '.join(home_stats.get('recent_form', []))}")
    
    with col2:
        st.write(f"**{away_team}**")
        st.write(f"Голы забито: {away_stats.get('goals_scored', 0)}")
        st.write(f"Голы пропущено: {away_stats.get('goals_conceded', 0)}")
        st.write(f"Форма: {' '.join(away_stats.get('recent_form', []))}")

def show_bet_management():
    """Управление ставками"""
    st.header("💰 Управление ставками")
    
    if st.session_state.betting_system is None:
        st.warning("Сначала инициализируйте систему")
        return
    
    # История ставок
    bet_history = st.session_state.betting_system.bankroll_manager.bet_history
    
    if bet_history:
        st.subheader("📋 История ставок")
        
        # Создаем DataFrame для отображения
        history_data = []
        for i, bet in enumerate(bet_history):
            history_data.append({
                'ID': i,
                'Дата': bet['timestamp'][:19],
                'Матч': f"{bet['match_info'].get('home_team', 'Team A')} vs {bet['match_info'].get('away_team', 'Team B')}",
                'Прогноз': bet['prediction'],
                'Ставка': f"{bet['bet_size']:.0f} ₽",
                'Коэффициент': f"{bet['odds']:.2f}",
                'Статус': bet.get('result', 'Ожидание'),
                'Банкролл': f"{bet.get('bankroll_after', bet['bankroll_before']):.0f} ₽"
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        # Разрешение ставок
        st.subheader("⚖️ Разрешение ставок")
        
        # Ставки, ожидающие разрешения
        pending_bets = [i for i, bet in enumerate(bet_history) if 'result' not in bet]
        
        if pending_bets:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                bet_id = st.selectbox(
                    "Выберите ставку:",
                    pending_bets,
                    format_func=lambda x: f"#{x}: {bet_history[x]['prediction']}"
                )
            
            with col2:
                result = st.selectbox("Результат:", ["Выигрыш", "Проигрыш"])
            
            with col3:
                if st.button("💾 Сохранить результат"):
                    won = result == "Выигрыш"
                    st.session_state.betting_system.resolve_bet(bet_id, won)
                    st.success("Результат сохранен!")
                    st.rerun()
        else:
            st.info("Нет ставок, ожидающих разрешения")
    else:
        st.info("История ставок пуста")

def show_statistics():
    """Статистика и аналитика"""
    st.header("📈 Статистика")
    
    if st.session_state.betting_system is None:
        st.warning("Сначала инициализируйте систему")
        return
    
    stats = st.session_state.betting_system.get_statistics()
    bankroll_stats = stats.get('bankroll_statistics', {})
    
    # Основные метрики
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("💰 Текущий банкролл", f"{bankroll_stats.get('current_bankroll', 0):,.0f} ₽")
        st.metric("📊 Всего ставок", bankroll_stats.get('total_bets', 0))
    
    with col2:
        st.metric("✅ Выигрышей", bankroll_stats.get('wins', 0))
        st.metric("❌ Проигрышей", bankroll_stats.get('losses', 0))
    
    with col3:
        st.metric("💹 ROI", f"{bankroll_stats.get('roi', 0):.1f}%")
        st.metric("🎯 Процент выигрышей", f"{bankroll_stats.get('win_rate', 0):.1f}%")
    
    # Графики
    if bankroll_stats.get('total_bets', 0) > 0:
        # Круговая диаграмма результатов
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥧 Распределение результатов")
            
            wins = bankroll_stats.get('wins', 0)
            losses = bankroll_stats.get('losses', 0)
            
            if wins + losses > 0:
                fig = px.pie(
                    values=[wins, losses],
                    names=['Выигрыши', 'Проигрыши'],
                    color_discrete_sequence=['green', 'red']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Финансовые показатели")
            
            profit_loss = bankroll_stats.get('profit_loss', 0)
            total_staked = bankroll_stats.get('total_staked', 1)
            
            fig = go.Figure(data=[
                go.Bar(name='Поставлено', x=['Финансы'], y=[total_staked], marker_color='blue'),
                go.Bar(name='Прибыль/Убыток', x=['Финансы'], y=[profit_loss], 
                       marker_color='green' if profit_loss >= 0 else 'red')
            ])
            
            fig.update_layout(barmode='group', title="Финансовые результаты")
            st.plotly_chart(fig, use_container_width=True)
    
    # Детальная информация
    st.subheader("📋 Детальная статистика")
    
    info_data = {
        'Показатель': [
            'Начальный банкролл',
            'Текущий банкролл', 
            'Изменение банкролла',
            'Всего поставлено',
            'Всего получено',
            'Чистая прибыль',
            'ROI',
            'Средняя ставка',
            'Последовательные проигрыши',
            'Стратегия'
        ],
        'Значение': [
            f"{Config.INITIAL_BANKROLL:,.0f} ₽",
            f"{bankroll_stats.get('current_bankroll', 0):,.0f} ₽",
            f"{bankroll_stats.get('bankroll_change', 0):,.0f} ₽",
            f"{bankroll_stats.get('total_staked', 0):,.0f} ₽",
            f"{bankroll_stats.get('total_returned', 0):,.0f} ₽",
            f"{bankroll_stats.get('profit_loss', 0):,.0f} ₽",
            f"{bankroll_stats.get('roi', 0):.2f}%",
            f"{bankroll_stats.get('total_staked', 0) / max(bankroll_stats.get('total_bets', 1), 1):,.0f} ₽",
            bankroll_stats.get('consecutive_losses', 0),
            bankroll_stats.get('strategy', 'N/A')
        ]
    }
    
    df_stats = pd.DataFrame(info_data)
    st.dataframe(df_stats, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main() 