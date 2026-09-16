export interface AppConfig {
	host: string;
	port: number;
	nodeEnv: string;
}

function parsePort(value: string | undefined): number {
	const port = Number(value ?? 3000);
	if (!Number.isInteger(port) || port < 1 || port > 65535) {
		throw new Error('PORT must be an integer between 1 and 65535');
	}
	return port;
}

export function loadConfig(environment: NodeJS.ProcessEnv = process.env): AppConfig {
	return {
		host: environment.HOST ?? '127.0.0.1',
		port: parsePort(environment.PORT),
		nodeEnv: environment.NODE_ENV ?? 'development'
	};
}
