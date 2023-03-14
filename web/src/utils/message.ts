import { ElMessage, MessageOptions } from 'element-plus';

export function message(message: string, option?: MessageOptions) {
	ElMessage({ message, ...option });
}
export function successMessage(message: string, option?: MessageOptions) {
	ElMessage({ message, ...option, type: 'success' });
}
export function warningMessage(message: string, option?: MessageOptions) {
	ElMessage({ message, ...option, type: 'warning' });
}
export function errorMessage(message: string, option?: MessageOptions) {
	ElMessage({ message, ...option, type: 'error' });
}
export function infoMessage(message: string, option?: MessageOptions) {
	ElMessage({ message, ...option, type: 'info' });
}
