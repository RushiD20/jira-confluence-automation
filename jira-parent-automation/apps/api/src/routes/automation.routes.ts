import { Router } from 'express';
import { PROJECT_KEY } from '../../../../packages/shared/constants';
import {
	AutomationEvent,
	EvaluationResult
} from '../../../../packages/shared/types';

export const automationRouter = Router();

function evaluateEvent(event: AutomationEvent): EvaluationResult {
	const base = { eventId: event.eventId, parentKey: event.parentKey };

	if (event.projectKey !== PROJECT_KEY) {
		return { ...base, action: 'ignored', reason: 'issue_outside_project' };
	}

	if (event.issueType !== 'sub-task' || !event.parentKey) {
		return { ...base, action: 'ignored', reason: 'issue_not_eligible_sub_task' };
	}

	if (event.destinationStatusCategory === 'done' && event.parentStatusCategory !== 'done') {
		const subTasks = event.parentSubTasks ?? [];
		if (subTasks.length === 0) {
			return { ...base, action: 'noop', reason: 'parent_has_no_sub_tasks' };
		}
		if (subTasks.some((subTask) => subTask.statusCategory !== 'done')) {
			return { ...base, action: 'noop', reason: 'sub_tasks_not_all_done' };
		}
		return { ...base, action: 'close', reason: 'all_sub_tasks_done' };
	}

	if (
		event.sourceStatusCategory === 'done' &&
		event.destinationStatusCategory !== 'done' &&
		event.parentStatusCategory === 'done'
	) {
		return { ...base, action: 'reopen', reason: 'sub_task_left_done' };
	}

	return { ...base, action: 'noop', reason: 'event_does_not_match_transition' };
}

automationRouter.post('/api/automation/evaluate', (request, response) => {
	const event = request.body as Partial<AutomationEvent>;
	if (!event || typeof event.eventId !== 'string' || typeof event.projectKey !== 'string') {
		response.status(400).json({ error: 'eventId and projectKey are required' });
		return;
	}

	response.status(200).json(evaluateEvent(event as AutomationEvent));
});
