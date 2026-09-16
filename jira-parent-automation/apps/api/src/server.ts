import express, { ErrorRequestHandler } from 'express';
import { loadConfig } from './config';
import { automationRouter } from './routes/automation.routes';
import { healthRouter } from './routes/health.routes';

export function createApp() {
	const app = express();
	app.use(express.json({ limit: '64kb' }));
	app.use(healthRouter);
	app.use(automationRouter);

	app.use((_request, response) => {
		response.status(404).json({ error: 'not_found' });
	});

	const errorHandler: ErrorRequestHandler = (error, _request, response, _next) => {
		console.error(error);
		response.status(500).json({ error: 'internal_server_error' });
	};
	app.use(errorHandler);

	return app;
}

if (require.main === module) {
	const config = loadConfig();
	createApp().listen(config.port, config.host, () => {
		console.log(`API listening on http://${config.host}:${config.port}`);
	});
}
