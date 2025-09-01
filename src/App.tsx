import { useState } from 'react'
import type { Screen, Problem, GameState } from './types'
import { sampleProblems } from './data/problems'
import { TitleScreen } from './components/TitleScreen'
import { ProblemSelect } from './components/ProblemSelect'
import { GameBoard } from './components/GameBoard'
import { ClearScreen } from './components/ClearScreen'
import { markProblemCleared } from './utils/storage'

function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('title')
  const [gameState, setGameState] = useState<GameState>({
    currentProblem: null,
    selectedTiles: [],
    topBelt: '',
    bottomBelt: '',
    gameMode: 'np-hard',
    isCompleted: false
  })

  const handleNavigate = (screen: Screen, gameMode?: 'np-hard' | 'undecidable') => {
    setCurrentScreen(screen)
    if (gameMode) {
      setGameState(prev => ({ ...prev, gameMode }))
    }
  }

  const handleSelectProblem = (problem: Problem) => {
    setGameState(prev => ({
      ...prev,
      currentProblem: problem,
      selectedTiles: [],
      topBelt: '',
      bottomBelt: '',
      isCompleted: false
    }))
  }

  const handleClear = () => {
    setGameState(prev => ({ ...prev, isCompleted: true }))
    
    // クリア状態を保存
    if (gameState.currentProblem) {
      markProblemCleared(gameState.currentProblem.id, gameState.gameMode)
    }
  }

  const handleNextProblem = () => {
    const currentProblems = sampleProblems.filter(p => p.difficulty === gameState.gameMode)
    const currentIndex = currentProblems.findIndex(p => p.id === gameState.currentProblem?.id)
    const nextProblem = currentProblems[currentIndex + 1]
    
    if (nextProblem) {
      handleSelectProblem(nextProblem)
      setCurrentScreen('game')
    }
  }

  const hasNextProblem = () => {
    if (!gameState.currentProblem) return false
    const currentProblems = sampleProblems.filter(p => p.difficulty === gameState.gameMode)
    const currentIndex = currentProblems.findIndex(p => p.id === gameState.currentProblem?.id)
    return currentIndex < currentProblems.length - 1
  }

  switch (currentScreen) {
    case 'title':
      return <TitleScreen onNavigate={handleNavigate} />
    
    case 'problem-select':
      return (
        <ProblemSelect
          problems={sampleProblems}
          gameMode={gameState.gameMode}
          onNavigate={handleNavigate}
          onSelectProblem={handleSelectProblem}
        />
      )
    
    case 'game':
      return gameState.currentProblem ? (
        <GameBoard
          problem={gameState.currentProblem}
          onNavigate={handleNavigate}
          onClear={handleClear}
        />
      ) : null
    
    case 'clear':
      return (
        <ClearScreen
          onNavigate={handleNavigate}
          onNextProblem={handleNextProblem}
          hasNextProblem={hasNextProblem()}
        />
      )
    
    default:
      return <TitleScreen onNavigate={handleNavigate} />
  }
}

export default App
