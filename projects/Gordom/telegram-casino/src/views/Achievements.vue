<template>
  <div class="achievements-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1 class="page-title">🏆 Достижения и квесты</h1>
      <div class="user-level">
        <div class="level-badge">
          <span class="level-number">{{ userLevel }}</span>
          <span class="level-label">Уровень</span>
        </div>
        <div class="xp-progress">
          <div class="xp-bar">
            <div class="xp-fill" :style="{ width: xpProgress + '%' }"></div>
          </div>
          <div class="xp-text">{{ currentXP }}/{{ nextLevelXP }} XP</div>
        </div>
      </div>
    </div>

    <!-- Статистика прогресса -->
    <div class="progress-stats">
      <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-value">{{ achievements.filter(a => a.unlocked).length }}</div>
        <div class="stat-label">Получено достижений</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-value">{{ totalXP }}</div>
        <div class="stat-label">Всего XP</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">🎮</div>
        <div class="stat-value">{{ activeQuests.filter(q => q.completed).length }}</div>
        <div class="stat-label">Выполненных квестов</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">💎</div>
        <div class="stat-value">{{ totalRewards }}</div>
        <div class="stat-label">Получено наград</div>
      </div>
    </div>

    <!-- Активные квесты -->
    <div class="active-quests">
      <h2 class="section-title">🎯 Активные квесты</h2>

      <div class="quests-grid">
        <div
          v-for="quest in activeQuests"
          :key="quest.id"
          class="quest-card"
          :class="{ 'completed': quest.completed, 'in-progress': quest.progress > 0 && !quest.completed }"
        >
          <div class="quest-header">
            <div class="quest-icon">{{ quest.icon }}</div>
            <div class="quest-info">
              <h4 class="quest-title">{{ quest.title }}</h4>
              <p class="quest-description">{{ quest.description }}</p>
            </div>
            <div class="quest-reward">
              <div class="reward-amount">+{{ quest.reward }} XP</div>
              <div v-if="quest.bonusReward" class="bonus-reward">
                +{{ quest.bonusReward }} ₽
              </div>
            </div>
          </div>

          <div class="quest-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: quest.progressPercent + '%' }"></div>
            </div>
            <div class="progress-text">
              {{ quest.currentProgress }}/{{ quest.targetProgress }}
            </div>
          </div>

          <div v-if="quest.completed" class="quest-completed">
            <div class="completed-icon">✅</div>
            <div class="completed-text">Выполнено!</div>
            <button @click="claimQuestReward(quest)" class="claim-btn" v-if="!quest.claimed">
              Получить награду
            </button>
            <div v-else class="claimed-text">Награда получена</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Достижения -->
    <div class="achievements-section">
      <h2 class="section-title">🏅 Достижения</h2>

      <div class="achievements-categories">
        <button
          v-for="category in achievementCategories"
          :key="category.id"
          @click="activeCategory = category.id"
          class="category-btn"
          :class="{ 'active': activeCategory === category.id }"
        >
          {{ category.icon }} {{ category.name }}
        </button>
      </div>

      <div class="achievements-grid">
        <div
          v-for="achievement in filteredAchievements"
          :key="achievement.id"
          class="achievement-card"
          :class="{ 'unlocked': achievement.unlocked, 'locked': !achievement.unlocked }"
        >
          <div class="achievement-icon">
            <span v-if="achievement.unlocked">{{ achievement.icon }}</span>
            <span v-else>🔒</span>
          </div>

          <div class="achievement-content">
            <h4 class="achievement-title">{{ achievement.title }}</h4>
            <p class="achievement-description">{{ achievement.description }}</p>

            <div class="achievement-progress" v-if="!achievement.unlocked">
              <div class="progress-bar small">
                <div class="progress-fill" :style="{ width: achievement.progressPercent + '%' }"></div>
              </div>
              <div class="progress-text small">
                {{ achievement.currentProgress }}/{{ achievement.targetProgress }}
              </div>
            </div>

            <div v-if="achievement.unlocked" class="achievement-unlocked">
              <div class="unlocked-date">
                Получено: {{ formatDate(achievement.unlockedDate) }}
              </div>
              <div class="achievement-reward">
                +{{ achievement.reward }} XP
              </div>
            </div>
          </div>

          <div class="achievement-rarity" :class="achievement.rarity">
            {{ achievement.rarity === 'common' ? 'Обычное' :
               achievement.rarity === 'rare' ? 'Редкое' :
               achievement.rarity === 'epic' ? 'Эпическое' :
               'Легендарное' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Доска лидеров -->
    <div class="leaderboard-section">
      <h2 class="section-title">📊 Таблица лидеров</h2>

      <div class="leaderboard-tabs">
        <button
          v-for="tab in leaderboardTabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="tab-btn"
          :class="{ 'active': activeTab === tab.id }"
        >
          {{ tab.icon }} {{ tab.name }}
        </button>
      </div>

      <div class="leaderboard-list">
        <div class="leaderboard-header">
          <div class="rank-column">#</div>
          <div class="player-column">Игрок</div>
          <div class="value-column">{{ activeTab === 'xp' ? 'XP' : activeTab === 'bets' ? 'Ставок' : 'Профит' }}</div>
          <div class="badge-column">Значок</div>
        </div>

        <div
          v-for="(player, index) in leaderboardData"
          :key="player.id"
          class="leaderboard-row"
          :class="{ 'current-user': player.isCurrentUser }"
        >
          <div class="rank-column">
            <div class="rank-number" :class="{ 'top': index < 3 }">
              {{ index + 1 }}
            </div>
          </div>

          <div class="player-column">
            <div class="player-avatar">
              <span>{{ player.name.charAt(0) }}</span>
            </div>
            <div class="player-info">
              <div class="player-name">{{ player.name }}</div>
              <div class="player-level">Уровень {{ player.level }}</div>
            </div>
          </div>

          <div class="value-column">
            <div class="value-number">{{ player.value }}</div>
            <div class="value-change" :class="{ 'positive': player.change > 0, 'negative': player.change < 0 }">
              <span v-if="player.change > 0">↗️</span>
              <span v-else-if="player.change < 0">↘️</span>
              <span v-else>➡️</span>
              {{ Math.abs(player.change) }}
            </div>
          </div>

          <div class="badge-column">
            <div class="player-badge" v-if="player.topBadge">
              {{ player.topBadge }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Ежедневные награды -->
    <div class="daily-rewards">
      <h2 class="section-title">🎁 Ежедневные награды</h2>

      <div class="daily-streak">
        <div class="streak-counter">
          <div class="streak-icon">🔥</div>
          <div class="streak-info">
            <div class="streak-days">{{ dailyStreak }}</div>
            <div class="streak-label">дней подряд</div>
          </div>
        </div>

        <div class="streak-rewards">
          <div
            v-for="day in 7"
            :key="day"
            class="streak-day"
            :class="{
              'completed': day <= dailyStreak,
              'current': day === dailyStreak + 1,
              'available': day === dailyStreak + 1
            }"
          >
            <div class="day-number">{{ day }}</div>
            <div class="day-reward">
              <span v-if="day <= 3">{{ day * 10 }} XP</span>
              <span v-else-if="day <= 5">{{ day * 25 }} XP</span>
              <span v-else-if="day === 6">{{ day * 50 }} XP</span>
              <span v-else>🎁 100 XP + 50₽</span>
            </div>
            <div v-if="day === dailyStreak + 1" class="claim-indicator">
              <button @click="claimDailyReward" class="claim-daily-btn">
                Получить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Achievements',
  data() {
    return {
      userLevel: 12,
      currentXP: 2450,
      nextLevelXP: 3000,
      totalXP: 12450,
      totalRewards: 1250,
      dailyStreak: 3,
      activeCategory: 'all',
      activeTab: 'xp',

      achievementCategories: [
        { id: 'all', name: 'Все', icon: '🏆' },
        { id: 'bets', name: 'Ставки', icon: '🎯' },
        { id: 'wins', name: 'Победы', icon: '🏅' },
        { id: 'sports', name: 'Спорт', icon: '⚽' },
        { id: 'esports', name: 'Киберспорт', icon: '🎮' },
        { id: 'special', name: 'Особые', icon: '⭐' }
      ],

      leaderboardTabs: [
        { id: 'xp', name: 'По XP', icon: '⚡' },
        { id: 'bets', name: 'По ставкам', icon: '🎯' },
        { id: 'profit', name: 'По профиту', icon: '💰' }
      ],

      achievements: [
        {
          id: 1,
          title: 'Первый шаг',
          description: 'Сделайте свою первую ставку',
          icon: '🚀',
          category: 'bets',
          rarity: 'common',
          targetProgress: 1,
          currentProgress: 1,
          unlocked: true,
          unlockedDate: '2024-01-15',
          reward: 50
        },
        {
          id: 2,
          title: 'Начинающий беттор',
          description: 'Сделайте 10 ставок',
          icon: '🎯',
          category: 'bets',
          rarity: 'common',
          targetProgress: 10,
          currentProgress: 10,
          unlocked: true,
          unlockedDate: '2024-01-16',
          reward: 100
        },
        {
          id: 3,
          title: 'Профессионал',
          description: 'Достигните win rate 60%',
          icon: '🏆',
          category: 'wins',
          rarity: 'epic',
          targetProgress: 60,
          currentProgress: 58,
          unlocked: false,
          reward: 500
        },
        {
          id: 4,
          title: 'Футбольный эксперт',
          description: 'Сделайте 50 ставок на футбол',
          icon: '⚽',
          category: 'sports',
          rarity: 'rare',
          targetProgress: 50,
          currentProgress: 45,
          unlocked: false,
          reward: 300
        },
        {
          id: 5,
          title: 'Киберспортивный гуру',
          description: 'Сделайте 25 ставок на киберспорт',
          icon: '🎮',
          category: 'esports',
          rarity: 'rare',
          targetProgress: 25,
          currentProgress: 25,
          unlocked: true,
          unlockedDate: '2024-01-20',
          reward: 250
        },
        {
          id: 6,
          title: 'Марафонец',
          description: 'Войдите в игру 7 дней подряд',
          icon: '🔥',
          category: 'special',
          rarity: 'epic',
          targetProgress: 7,
          currentProgress: 7,
          unlocked: true,
          unlockedDate: '2024-01-18',
          reward: 400
        }
      ],

      activeQuests: [
        {
          id: 1,
          title: 'Ежедневная ставка',
          description: 'Сделайте 3 ставки сегодня',
          icon: '🎯',
          targetProgress: 3,
          currentProgress: 2,
          progressPercent: 66,
          completed: false,
          claimed: false,
          reward: 50,
          bonusReward: 25
        },
        {
          id: 2,
          title: 'Победная серия',
          description: 'Выиграйте 5 ставок подряд',
          icon: '🏅',
          targetProgress: 5,
          currentProgress: 3,
          progressPercent: 60,
          completed: false,
          claimed: false,
          reward: 150,
          bonusReward: 75
        },
        {
          id: 3,
          title: 'Исследователь',
          description: 'Попробуйте ставки на 3 разных вида спорта',
          icon: '🌍',
          targetProgress: 3,
          currentProgress: 1,
          progressPercent: 33,
          completed: false,
          claimed: false,
          reward: 100,
          bonusReward: 50
        },
        {
          id: 4,
          title: 'Крупный выигрыш',
          description: 'Выиграйте ставку с коэффициентом выше 3.0',
          icon: '💎',
          targetProgress: 1,
          currentProgress: 1,
          progressPercent: 100,
          completed: true,
          claimed: false,
          reward: 200,
          bonusReward: 100
        }
      ],

      leaderboardData: [
        { id: 1, name: 'ProGamer', level: 25, value: 15420, change: 120, isCurrentUser: false, topBadge: '🏆' },
        { id: 2, name: 'BetMaster', level: 22, value: 12850, change: -50, isCurrentUser: false, topBadge: '🥇' },
        { id: 3, name: 'LuckyStrike', level: 20, value: 11200, change: 200, isCurrentUser: false, topBadge: '🥈' },
        { id: 4, name: 'SportKing', level: 18, value: 8900, change: 75, isCurrentUser: false, topBadge: '🥉' },
        { id: 5, name: 'WinMachine', level: 16, value: 7560, change: -20, isCurrentUser: true, topBadge: '⚡' },
        { id: 6, name: 'BetQueen', level: 15, value: 6890, change: 150, isCurrentUser: false, topBadge: '🔥' },
        { id: 7, name: 'LuckyBet', level: 14, value: 5420, change: 80, isCurrentUser: false, topBadge: '💎' }
      ]
    }
  },
  computed: {
    xpProgress() {
      return (this.currentXP / this.nextLevelXP) * 100
    },

    filteredAchievements() {
      if (this.activeCategory === 'all') {
        return this.achievements
      }
      return this.achievements.filter(a => a.category === this.activeCategory)
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      })
    },

    claimQuestReward(quest) {
      quest.claimed = true
      this.currentXP += quest.reward
      this.totalXP += quest.reward

      // Проверяем повышение уровня
      this.checkLevelUp()

      // Показываем уведомление
      this.$emit('show-notification', {
        type: 'success',
        title: 'Награда получена!',
        message: `+${quest.reward} XP ${quest.bonusReward ? `+${quest.bonusReward} ₽` : ''}`
      })
    },

    claimDailyReward() {
      const rewards = [10, 20, 30, 50, 75, 100, 150]
      const reward = rewards[this.dailyStreak] || 50

      this.currentXP += reward
      this.totalXP += reward
      this.dailyStreak++

      this.checkLevelUp()

      this.$emit('show-notification', {
        type: 'success',
        title: 'Ежедневная награда!',
        message: `+${reward} XP за ${this.dailyStreak} день подряд`
      })
    },

    checkLevelUp() {
      while (this.currentXP >= this.nextLevelXP) {
        this.userLevel++
        this.currentXP -= this.nextLevelXP
        this.nextLevelXP = Math.floor(this.nextLevelXP * 1.2)

        this.$emit('show-notification', {
          type: 'promotion',
          title: 'Повышение уровня!',
          message: `Поздравляем! Вы достигли ${this.userLevel} уровня!`
        })
      }
    }
  }
}
</script>

<style scoped>
.achievements-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  color: white;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.1);
  padding: 25px;
  border-radius: 20px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  background: linear-gradient(45deg, #fff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-level {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.level-badge {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #333;
  font-weight: 800;
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
}

.level-number {
  font-size: 1.5rem;
  line-height: 1;
}

.level-label {
  font-size: 0.7rem;
  opacity: 0.8;
}

.xp-progress {
  width: 200px;
}

.xp-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
}

.xp-fill {
  height: 100%;
  background: linear-gradient(90deg, #ffd700 0%, #ff6b6b 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.xp-text {
  font-size: 0.8rem;
  opacity: 0.8;
  text-align: center;
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 10px;
  opacity: 0.8;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 500;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #fff;
}

.active-quests {
  margin-bottom: 30px;
}

.quests-grid {
  display: grid;
  gap: 20px;
}

.quest-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 25px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.quest-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.quest-card.completed {
  border-left: 4px solid #28a745;
  background: rgba(40, 167, 69, 0.1);
}

.quest-card.in-progress {
  border-left: 4px solid #ffc107;
  background: rgba(255, 193, 7, 0.1);
}

.quest-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.quest-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.quest-info {
  flex: 1;
}

.quest-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 5px;
}

.quest-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.4;
}

.quest-reward {
  text-align: right;
}

.reward-amount {
  font-size: 1rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 5px;
}

.bonus-reward {
  font-size: 0.9rem;
  color: #28a745;
  font-weight: 600;
}

.quest-progress {
  margin-bottom: 15px;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.8rem;
  opacity: 0.8;
  text-align: center;
}

.quest-completed {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: rgba(40, 167, 69, 0.1);
  border-radius: 10px;
}

.completed-icon {
  font-size: 1.2rem;
}

.completed-text {
  font-weight: 600;
  color: #28a745;
  flex: 1;
}

.claim-btn {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.claim-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.claimed-text {
  font-size: 0.9rem;
  color: #28a745;
  font-weight: 600;
}

.achievements-section {
  margin-bottom: 30px;
}

.achievements-categories {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.category-btn {
  padding: 10px 20px;
  border-radius: 25px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.category-btn.active {
  background: #667eea;
  border-color: #667eea;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.achievement-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.achievement-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.achievement-card.unlocked {
  border-left: 4px solid #28a745;
}

.achievement-card.locked {
  opacity: 0.7;
}

.achievement-card.common::before { background: linear-gradient(90deg, #6c757d, #adb5bd); }
.achievement-card.rare::before { background: linear-gradient(90deg, #007bff, #0056b3); }
.achievement-card.epic::before { background: linear-gradient(90deg, #6f42c1, #5a32a3); }
.achievement-card.legendary::before { background: linear-gradient(90deg, #fd7e14, #e8680d); }

.achievement-icon {
  font-size: 2rem;
  margin-bottom: 15px;
  text-align: center;
}

.achievement-content {
  margin-bottom: 15px;
}

.achievement-title {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 8px;
}

.achievement-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.4;
  margin-bottom: 15px;
}

.achievement-progress {
  margin-bottom: 15px;
}

.progress-bar.small {
  height: 6px;
}

.progress-text.small {
  font-size: 0.7rem;
}

.achievement-unlocked {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.unlocked-date {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-bottom: 5px;
}

.achievement-reward {
  font-size: 0.9rem;
  font-weight: 600;
  color: #ffd700;
}

.achievement-rarity {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 10px;
  text-transform: uppercase;
}

.achievement-rarity.common { background: rgba(108, 117, 125, 0.2); color: #6c757d; }
.achievement-rarity.rare { background: rgba(0, 123, 255, 0.2); color: #007bff; }
.achievement-rarity.epic { background: rgba(111, 66, 193, 0.2); color: #6f42c1; }
.achievement-rarity.legendary { background: rgba(253, 126, 20, 0.2); color: #fd7e14; }

.leaderboard-section {
  margin-bottom: 30px;
}

.leaderboard-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 20px;
  border-radius: 25px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

.tab-btn.active {
  background: #667eea;
  border-color: #667eea;
}

.leaderboard-list {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.leaderboard-header {
  display: grid;
  grid-template-columns: 60px 1fr 100px 80px;
  gap: 15px;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.1);
  font-weight: 600;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
}

.leaderboard-row {
  display: grid;
  grid-template-columns: 60px 1fr 100px 80px;
  gap: 15px;
  padding: 15px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.leaderboard-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.leaderboard-row.current-user {
  background: rgba(102, 126, 234, 0.1);
  border-left: 4px solid #667eea;
}

.leaderboard-row:last-child {
  border-bottom: none;
}

.rank-column {
  display: flex;
  align-items: center;
  justify-content: center;
}

.rank-number {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
}

.rank-number.top {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.player-column {
  display: flex;
  align-items: center;
  gap: 12px;
}

.player-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: white;
}

.player-info {
  flex: 1;
}

.player-name {
  font-weight: 600;
  color: #fff;
  margin-bottom: 2px;
}

.player-level {
  font-size: 0.8rem;
  opacity: 0.7;
}

.value-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.value-number {
  font-size: 1rem;
  font-weight: 700;
  color: #ffd700;
}

.value-change {
  font-size: 0.7rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 2px;
}

.value-change.positive { color: #28a745; }
.value-change.negative { color: #dc3545; }

.badge-column {
  display: flex;
  align-items: center;
  justify-content: center;
}

.player-badge {
  font-size: 1.2rem;
}

.daily-rewards {
  margin-bottom: 30px;
}

.daily-streak {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 25px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.streak-counter {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.streak-icon {
  font-size: 2rem;
}

.streak-info {
  flex: 1;
}

.streak-days {
  font-size: 2rem;
  font-weight: 800;
  color: #ffd700;
}

.streak-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.streak-rewards {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
}

.streak-day {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 15px 10px;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  position: relative;
}

.streak-day.completed {
  background: rgba(40, 167, 69, 0.2);
  border: 2px solid #28a745;
}

.streak-day.current {
  background: rgba(255, 193, 7, 0.2);
  border: 2px solid #ffc107;
  animation: pulse 2s infinite;
}

.streak-day.available {
  background: rgba(0, 123, 255, 0.2);
  border: 2px solid #007bff;
  cursor: pointer;
}

.streak-day.available:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
}

.day-number {
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
}

.day-reward {
  font-size: 0.8rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  text-align: center;
}

.streak-day.completed .day-reward {
  color: #28a745;
}

.streak-day.current .day-reward {
  color: #ffc107;
}

.streak-day.available .day-reward {
  color: #007bff;
}

.claim-daily-btn {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.claim-daily-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .achievements-page {
    padding: 15px;
  }

  .page-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  .user-level {
    flex-direction: row;
    justify-content: center;
  }

  .xp-progress {
    width: 150px;
  }

  .progress-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .achievements-grid {
    grid-template-columns: 1fr;
  }

  .leaderboard-header,
  .leaderboard-row {
    grid-template-columns: 50px 1fr 80px 60px;
  }

  .streak-rewards {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 480px) {
  .progress-stats {
    grid-template-columns: 1fr;
  }

  .streak-rewards {
    grid-template-columns: repeat(3, 1fr);
  }

  .quests-grid {
    gap: 15px;
  }

  .quest-card {
    padding: 20px;
  }
}
</style>