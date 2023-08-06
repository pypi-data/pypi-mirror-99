from django.utils import timezone
from django.db import transaction

from wis_queue_manager.models import FileProcessingTask, FileIndexingTask, FileDecompressionTask, FileDiffTask


class QueueManager(object):
    @staticmethod
    def get_next_data_processing_task():
        with transaction.atomic():
            file_processing_task = (
                FileProcessingTask
                .objects
                .select_for_update(skip_locked=True)
                .filter(status=FileProcessingTask.TODO)
                .order_by('processing_priority', 'id')
                .first()
            )
            if file_processing_task:
                file_processing_task.status = FileProcessingTask.IN_PROGRESS
                file_processing_task.start_time = timezone.now()
                file_processing_task.last_updated = file_processing_task.start_time
                file_processing_task.finish_time = None
                file_processing_task.duration = None
                file_processing_task.records_processed = 0
                file_processing_task.records_processed_per_second = None
                file_processing_task.save()
        return file_processing_task

    @staticmethod
    def get_next_data_indexing_task():
        with transaction.atomic():
            file_indexing_task = (
                FileIndexingTask
                    .objects
                    .select_for_update(skip_locked=True)
                    .filter(status = FileIndexingTask.TODO)
                    .first()
            )

            if file_indexing_task:
                file_indexing_task.status = FileIndexingTask.IN_PROGRESS
                file_indexing_task.start_time = timezone.now()
                file_indexing_task.last_updated = file_indexing_task.start_time
                file_indexing_task.finish_time = None
                file_indexing_task.duration = None
                file_indexing_task.records_processed = 0
                file_indexing_task.records_processed_per_second = None
                file_indexing_task.save()
            return file_indexing_task

    @staticmethod
    def get_next_data_decompression_task():
        with transaction.atomic():
            file_decompression_task = (
                FileDecompressionTask
                    .objects
                    .select_for_update(skip_locked=True)
                    .filter(status = FileDecompressionTask.TODO)
                    .order_by('processing_priority', '-file_size')
                    .first()
            )

            if file_decompression_task:
                file_decompression_task.status = FileDecompressionTask.IN_PROGRESS
                file_decompression_task.start_time = timezone.now()
                file_decompression_task.last_updated = file_decompression_task.start_time
                file_decompression_task.finish_time = None
                file_decompression_task.duration = None
                file_decompression_task.records_processed = 0
                file_decompression_task.records_processed_per_second = None
                file_decompression_task.save()
            return file_decompression_task

    @staticmethod
    def get_next_file_diff_task():
        with transaction.atomic():
            file_diff_task = (
                FileDiffTask
                    .objects
                    .select_for_update(skip_locked=True)
                    .filter(status = FileDiffTask.TODO)
                    .first()
            )

            if file_diff_task:
                file_diff_task.status = FileDiffTask.IN_PROGRESS
                file_diff_task.start_time = timezone.now()
                file_diff_task.last_updated = file_diff_task.start_time
                file_diff_task.finish_time = None
                file_diff_task.duration = None
                file_diff_task.records_processed = 0
                file_diff_task.records_processed_per_second = None
                file_diff_task.save()
            return file_diff_task

