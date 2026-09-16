export type StatusCategory = 'todo' | 'in_progress' | 'done';

export type EvaluationAction = 'close' | 'reopen' | 'noop' | 'ignored';

export interface SubTaskStatus {
	key: string;
	statusCategory: StatusCategory;
}

export interface AutomationEvent {
	eventId: string;
	projectKey: string;
	issueKey: string;
	issueType: 'sub-task' | 'other';
	parentKey?: string;
	sourceStatusCategory: StatusCategory;
	destinationStatusCategory: StatusCategory;
	parentStatusCategory?: StatusCategory;
	parentSubTasks?: SubTaskStatus[];
}

export interface EvaluationResult {
	action: EvaluationAction;
	reason: string;
	eventId: string;
	parentKey?: string;
}
