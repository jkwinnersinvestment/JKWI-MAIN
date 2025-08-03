export const formatDate = (dateString: string): string => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

export const calculatePercentage = (part: number, total: number): string => {
    if (total === 0) return '0%';
    const percentage = (part / total) * 100;
    return `${percentage.toFixed(2)}%`;
};

export const generateUniqueId = (): string => {
    return 'id-' + Math.random().toString(36).substr(2, 9);
};