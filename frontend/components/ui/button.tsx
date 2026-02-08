import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline';
    size?: 'sm' | 'md' | 'lg';
}

export function Button({
    className,
    variant = 'primary',
    size = 'md',
    children,
    ...props
}: ButtonProps) {
    const baseStyles = 'rounded-lg font-semibold transition-all';

    const variants = {
        primary: 'bg-purple-600 hover:bg-purple-700 text-white',
        secondary: 'bg-white/10 hover:bg-white/20 text-white border border-white/20',
        outline: 'border-2 border-purple-600 text-purple-600 hover:bg-purple-600 hover:text-white',
    };

    const sizes = {
        sm: 'px-4 py-2 text-sm',
        md: 'px-6 py-3 text-base',
        lg: 'px-8 py-4 text-lg',
    };

    return (
        <button
            className={cn(baseStyles, variants[variant], sizes[size], className)}
            {...props}
        >
            {children}
        </button>
    );
}
