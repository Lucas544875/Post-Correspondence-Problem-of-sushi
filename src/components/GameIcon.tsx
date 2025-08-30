import sashimiImg from '../assets/sashimi.png';
import tampopoImg from '../assets/tampopo.png';

interface GameIconProps {
  type: 'sashimi' | 'tampopo';
  size?: 'small' | 'medium' | 'large' | 'relative';
  className?: string;
  style?: React.CSSProperties;
}

export const GameIcon = ({ type, size = 'medium', className = '', style }: GameIconProps) => {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-8 h-8', 
    large: 'w-12 h-12',
    relative: "max-w-12 max-h-12 min-w-0",
  };

  const src = type === 'sashimi' ? sashimiImg : tampopoImg;
  const alt = type === 'sashimi' ? '刺身' : 'タンポポ';

  return (
    <img 
      src={src} 
      alt={alt}
      className={`inline-block ${sizeClasses[size]} ${className}`}
      style={style}
    />
  );
};