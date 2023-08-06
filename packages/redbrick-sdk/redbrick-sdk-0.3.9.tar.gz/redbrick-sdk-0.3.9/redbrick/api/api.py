"""Getting data from redbrick api."""

import redbrick
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Union, Tuple
import requests
import numpy as np  # type: ignore
import cv2  # type: ignore
from redbrick.utils import url_to_image
from .api_base import RedBrickApiBase
from redbrick.entity.custom_group import CustomGroup
from redbrick.entity.datapoint import Image
from redbrick.entity.datapoint import Video
from redbrick.entity.task import Task
from redbrick.entity.taxonomy2 import Taxonomy2


class RedBrickApi(RedBrickApiBase):
    """Implement Abstract API."""

    def __init__(self, cache: bool = False, custom_url: Optional[str] = None) -> None:
        """Construct RedBrickApi."""
        self.client = redbrick.client.RedBrickClient()
        if custom_url:
            self.url = custom_url
        elif self.client.custom_url:
            self.url = self.client.custom_url
        else:
            self.url = (
                "https://ck7r1z68k7.execute-api.us-east-1.amazonaws.com/prod/graphql/"
            )

    def get_datapointset(self, org_id: str, data_set_name: str) -> Dict:
        """Get dataset specified by org_id and dataset_name"""
        query_string = """
            query ($orgId:UUID!, $name:String!) {
                dataPointSet(orgId: $orgId, name: $name){
                    orgId
                    name
                    dataType
                    datapointCount
                    desc
                    createdAt
                    createdBy
                    status
                }
            }
        """
        query_variables = {"orgId": org_id, "name": data_set_name}
        query = dict(query=query_string, variables=query_variables)

        result = self._execute_query(query)
        return result

    def get_itemListUploadPresign(self, org_id: str, file_name: str) -> Dict:
        """Get a presigned URL to upload files to."""
        query_string = """
            query ($orgId: UUID!, $name: String!){
                itemListUploadPresign(orgId: $orgId, fileName: $name){
                    presignedUrl
                    filePath
                    fileName
                    uploadId
                    createdAt
                }
            }
        """

        query_variables = {"orgId": org_id, "name": file_name}
        query = dict(query=query_string, variables=query_variables)

        result = self._execute_query(query)

        return result

    def itemListUploadSuccess(
        self, org_id: str, itemsListUploadSuccessInput: Dict,
    ) -> Dict:
        """Calls backend to process uploaded item list."""
        query_string = """
            mutation($orgId: UUID!, $payload: ItemsListUploadSuccessInput!){
                itemListUploadSuccess(orgId: $orgId, payload: $payload){
                    ok
                    upload{
                        orgId
                        importId
                        datapointCount
                        dataType
                        taskType
                        filePath
                        createdAt
                        createdBy
                        status
                        statusMsg
                    }
                }
            }
        """

        query_variables = {"orgId": org_id, "payload": itemsListUploadSuccessInput}
        query = dict(query=query_string, variables=query_variables)

        result = self._execute_query(query)

        return result

    def createDatapoint(
        self,
        org_id: str,
        items: List[str],
        name: str,
        data_set_name: str,
        storage_id: str,
        label_set_name: str = None,
        labels: List[Dict] = None,
    ) -> Dict:
        """Calls backend to create a datapoint."""
        query_string = """
            mutation(
                $orgId: UUID!
                $items: [String!]!
                $name: String!
                $dsetName: String!
                $storageId: UUID!
                $lsetName: String
                $labels: [LabelInput!]
            ) {
                createDatapoint(
                    orgId: $orgId
                    items: $items
                    name: $name
                    dsetName: $dsetName
                    storageId: $storageId
                    lsetName: $lsetName
                    labels: $labels
                ) {
                    dpId
                }
            }
        """

        query_variables = {
            "orgId": org_id,
            "items": items,
            "name": name,
            "dsetName": data_set_name,
            "storageId": storage_id,
            "lsetName": label_set_name,
            "labels": labels,
        }

        if label_set_name is not None:
            query_variables["lsetName"] = label_set_name
            query_variables["labels"] = labels

        query = dict(query=query_string, variables=query_variables)

        result = self._execute_query(query)

        return result

    def get_datapoint_ids(
        self, org_id: str, label_set_name: str
    ) -> Tuple[List[str], CustomGroup]:
        """Get a list of datapoint ids in labelset."""
        query_string = """
            query ($orgId:UUID!, $name:String!) {
                customGroup(orgId: $orgId, name: $name) {
                    datapoints(skip:0, first:-1) {
                        dpId
                    }
                    taskType,
                    dataType
                    taxonomy {
                    name
                    version
                    categories {
                        name
                        children {
                        name
                        classId
                        children {
                            name
                            classId
                            children {
                            name
                            classId
                            }
                        }
                        }
                    }
                    }
                }
            }
        """
        query_variables = {"orgId": org_id, "name": label_set_name}
        query = dict(query=query_string, variables=query_variables)

        result = self._execute_query(query)

        all_dp_ids = [dp["dpId"] for dp in result["customGroup"]["datapoints"]]
        custom_group = CustomGroup(
            result["customGroup"]["taskType"],
            result["customGroup"]["dataType"],
            result["customGroup"]["taxonomy"],
        )
        return all_dp_ids, custom_group

    def get_datapoint(
        self,
        org_id: str,
        label_set_name: str,
        dp_id: str,
        task_type: str,
        taxonomy: dict,
    ) -> Union[Image, Video]:
        """Get all relevant information related to a datapoint."""
        query_string = """
            query ($orgId: UUID!, $dpId: UUID!, $name:String!) {
                labelData(orgId: $orgId, dpId: $dpId, customGroupName: $name) {
                    blob
                    dataPoint {
                        items:items(presigned:true)
                        items_not_signed:items(presigned:false)
                        name
                    },
                    createdBy,
                    taskType,
                    dataType,
                    labels {
                      category,
                      attributes {
                        ... on LabelAttributeInt {
                        name
                        valint: value
                        }
                        ... on LabelAttributeBool {
                        name
                        valbool: value
                        }
                        ... on LabelAttributeFloat {
                        name
                        valfloat: value
                        }
                        ... on LabelAttributeString {
                        name
                        valstr: value
                        }
                      }
                      labelid,
                      frameclassify,
                      frameindex,
                      trackid,
                      keyframe,
                      end,
                      bbox2d {
                          xnorm,
                          ynorm,
                          wnorm,
                          hnorm,
                      },
                      pixel {
                          imagesize,
                          regions,
                          holes
                      }
                    }
                }
            }
        """
        # EXECUTE THE QUERY
        query_variables = {"orgId": org_id, "name": label_set_name, "dpId": dp_id}
        query = dict(query=query_string, variables=query_variables)
        result = self._execute_query(query)

        # IMAGE DATA
        if result["labelData"]["dataType"] == "IMAGE":
            # Parse result
            # print("RESULT", result)
            with open("temp.json", "w+") as file:
                json.dump(result, file, indent=2)
            signed_image_url = result["labelData"]["dataPoint"]["items"][0]
            unsigned_image_url = result["labelData"]["dataPoint"]["items_not_signed"][0]
            labels = result["labelData"]["labels"]
            created_by = result["labelData"]["createdBy"]
            image_data = url_to_image(signed_image_url)  # Get image array

            dpoint = Image(
                created_by=created_by,
                org_id=org_id,
                label_set_name=label_set_name,
                taxonomy=taxonomy,
                remote_labels=labels,
                dp_id=dp_id,
                image_url=signed_image_url,
                image_url_not_signed=unsigned_image_url,
                image_data=image_data,
                task_type=task_type,
            )
            return dpoint

        # VIDEO DATA
        else:
            # Parse the result
            items = result["labelData"]["dataPoint"]["items"]
            items_not_signed = result["labelData"]["dataPoint"]["items_not_signed"]
            labels = result["labelData"]["labels"]
            with open("result.json", "w+") as file:
                json.dump(result, file, indent=2)
            name = result["labelData"]["dataPoint"]["name"]
            dpoint_vid = Video(
                org_id=org_id,
                label_set_name=label_set_name,
                taxonomy=taxonomy,
                task_type=task_type,
                remote_labels=labels,
                dp_id=dp_id,
                video_name=name,
                items_list=items,
                items_list_not_signed=items_not_signed,
            )
            return dpoint_vid

    def get_datapoints_paged(
        self,
        org_id: str,
        label_set_name: str,
        cursor: Optional[str] = None,
        first: int = 50,
    ) -> dict:
        """Get all relevant information related to a datapoint."""
        query_string = """
        query ($orgId: UUID!, $name: String!,$first: Int, $cursor: String){
        customGroup(orgId: $orgId, name:$name){
            orgId
            name
            dataType
            taskType
            taxonomy {
            categories {
                name
                children{
                name
                classId
                children {
                    name
                    classId
                    children {
                    name
                    classId
                    }
                }
                }

            }
            }
            datapointCount
            datapointsPaged(first:$first, after:$cursor) {
            entries {
                dpId
                name
                itemsPresigned:items (presigned:true)
                items(presigned:false)
                labelData(customGroupName: $name){
                createdByEmail
                labels {
                    category
                    attributes {
                        ... on LabelAttributeInt {
                        name
                        valint: value
                        }
                        ... on LabelAttributeBool {
                        name
                        valbool: value
                        }
                        ... on LabelAttributeFloat {
                        name
                        valfloat: value
                        }
                        ... on LabelAttributeString {
                        name
                        valstr: value
                        }
                    }
                    labelid
                    frameindex
                    trackid
                    keyframe
                    taskclassify
                    frameclassify
                    end
                    bbox2d {
                        xnorm
                        ynorm
                        wnorm
                        hnorm
                    }
                    point {
                        xnorm
                        ynorm
                    }
                    polyline {
                        xnorm
                        ynorm
                    }
                    polygon {
                        xnorm
                        ynorm
                    }
                    pixel {
                        imagesize
                        regions
                        holes
                    }
                    ellipse {
                        xcenternorm
                        ycenternorm
                        xnorm
                        ynorm
                        rot
                    }
                    }
                }


            }
            cursor
            }
        }
        }

        """
        # EXECUTE THE QUERY
        query_variables = {
            "orgId": org_id,
            "name": label_set_name,
            "cursor": cursor,
            "first": first,
        }
        query = dict(query=query_string, variables=query_variables)
        result = self._execute_query(query)
        return result

    def tasksToLabelRemote(self, orgId, projectId, stageName, numTasks) -> List[Task]:
        """Get remote labeling tasks."""
        query_string = """
        query ($orgId:UUID!, $projectId:UUID!, $stageName:String!, $numTasks:Int!){
            tasksToLabelRemote(orgId:$orgId, projectId:$projectId, stageName:$stageName, numTasks:$numTasks) {
                stageName,
                taskId,
                subName,
                modelName,
                createdAt,
                dpId,
                taxonomy {
                    name,
                    version,
                    categories {
                        name,
                        children {
                            name,
                            classId,
                            children {
                                name,
                                classId,
                                children {
                                    name,
                                    classId
                                }
                            }
                        }
                    }
                }
                datapoint {
                    items(presigned:false),
                    itemsPresigned,
                }
            }
        }
        """
        query_variables = {
            "orgId": orgId,
            "projectId": projectId,
            "stageName": stageName,
            "numTasks": numTasks,
        }
        query = dict(query=query_string, variables=query_variables)
        result = self._execute_query(query)
        result = result["tasksToLabelRemote"]

        # Get stage information
        stage_info = self.get_stage(orgId, projectId, stageName)

        tasks = []
        for res in result:
            # Create a task object and return
            task = Task(
                org_id=orgId,
                project_id=projectId,
                stage_name=stageName,
                task_id=res["taskId"],
                dp_id=res["dpId"],
                sub_name=res["subName"],
                taxonomy=res["taxonomy"],
                items_list=res["datapoint"]["items"],
                items_list_presigned=res["datapoint"]["itemsPresigned"],
                task_data_type=stage_info["outputType"],
            )
            tasks.append(task)

        return tasks

    def putTaskData(
        self,
        org_id,
        project_id,
        dp_id,
        stage_name,
        sub_name,
        task_data,
        taxonomy_name,
        taxonomy_version,
        td_type,
        augmentdata=None,
    ) -> None:
        """Put task data for a labeling task."""
        query_string = """
        mutation($orgId:UUID!, $dpId:UUID!, $projectId:UUID!, $stageName:String!, $subName:String!, $taskData:JSONString!, $taxonomyName: String!, $taxonomyVersion: Int!, $tdType: TaskDataType!) {
            putTaskData(orgId:$orgId, dpId:$dpId, projectId: $projectId, stageName:$stageName, subName:$subName, taskData:$taskData, taxonomyName:$taxonomyName, taxonomyVersion: $taxonomyVersion, tdType:$tdType) {
                ok
            }
        }
        """
        query_variables = {
            "orgId": org_id,
            "projectId": project_id,
            "dpId": dp_id,
            "stageName": stage_name,
            "subName": sub_name,
            "taskData": task_data,
            "taxonomyName": taxonomy_name,
            "taxonomyVersion": taxonomy_version,
            "tdType": td_type,
        }
        query = dict(query=query_string, variables=query_variables)
        self._execute_query(query)

    def putLabels(
        self,
        org_id,
        project_id,
        dp_id,
        stage_name,
        sub_name,
        labels,
        taxonomy_name,
        taxonomy_version,
        td_type,
        augmentdata=None,
    ) -> None:
        """Put task data for a labeling task."""
        query_string = """
        mutation($orgId:UUID!, $dpId:UUID!, $projectId:UUID!, $stageName:String!, $subName:String!, $labels:[LabelInput]!, $taxonomyName: String!, $taxonomyVersion: Int!, $tdType: TaskDataType!) {
            putLabels(orgId:$orgId, dpId:$dpId, projectId: $projectId, stageName:$stageName, subName:$subName, labels:$labels, taxonomyName:$taxonomyName, taxonomyVersion: $taxonomyVersion, tdType:$tdType) {
                ok
            }
        }
        """
        query_variables = {
            "orgId": org_id,
            "projectId": project_id,
            "dpId": dp_id,
            "stageName": stage_name,
            "subName": sub_name,
            "labels": labels,
            "taxonomyName": taxonomy_name,
            "taxonomyVersion": taxonomy_version,
            "tdType": td_type,
        }
        query = dict(query=query_string, variables=query_variables)
        self._execute_query(query)

    def putRemoteLabelingTask(self, finishedTask) -> None:
        """Put remote labeling task to backend."""
        query_string = """
        mutation($finishedTask: RemoteLabelingTaskInput!) {
            putRemoteLabelingTask(finishedTask: $finishedTask) {
                ok
            }
        }
        """

        query_variables = {"finishedTask": finishedTask}
        query = dict(query=query_string, variables=query_variables)
        self._execute_query(query)

    def putRemoteLabelingTasksAndLabels(
        self, org_id, project_id, stage_name, finished_tasks
    ) -> None:
        """Put remote labeling tasks and labels to backend."""
        query_string = """
            mutation($orgId: UUID!, $projectId: UUID!, $stageName: String!, $finishedTasks: [RemoteLabelingTaskWithLabelsInput!]!) {
                putRemoteLabelingTasksAndLabels(
                    orgId: $orgId
                    projectId: $projectId
                    stageName: $stageName
                    finishedTasks: $finishedTasks
                ){
                    ok
                }
            }
        """
        query_variables = {
            "orgId": org_id,
            "projectId": project_id,
            "stageName": stage_name,
            "finishedTasks": finished_tasks,
        }
        query = dict(query=query_string, variables=query_variables)
        self._execute_query(query)

    def get_stage(self, org_id, project_id, stage_name) -> Dict[Any, Any]:
        """Get stage information."""
        query_string = """
            query($orgId: UUID!, $projectId: UUID!, $stageName: String!) {
                stage(orgId: $orgId, projectId: $projectId, stageName: $stageName) {
                    inputType,
                    outputType,
                    outputTaxonomyName,
                    outputTaxonomyVersion
                }
            }
        """
        query_variables = {
            "orgId": org_id,
            "projectId": project_id,
            "stageName": stage_name,
        }
        query = dict(query=query_string, variables=query_variables)
        result = self._execute_query(query)
        return result["stage"]

    def get_num_remote_tasks(self, org_id, project_id, stage_name) -> int:
        """Get stage information."""
        query_string = """
        query($orgId: UUID!, $projectId: UUID!, $stageName: String!) {
            stageStat(orgId: $orgId, projectId: $projectId, stageName: $stageName) {
                currentTaskCount
            }
        }
        """
        query_variables = {
            "orgId": org_id,
            "projectId": project_id,
            "stageName": stage_name,
        }
        query = dict(query=query_string, variables=query_variables)
        result = self._execute_query(query)
        return int(result["stageStat"]["currentTaskCount"])

    def get_taxonomy(self, orgId: str, name: str, version: int) -> Taxonomy2:
        """Get a taxonomy info."""
        query_string = """
        query ($orgId: UUID!, $name: String!, $version: Int!) {
            taxonomy(orgId: $orgId, name: $name, version: $version) {
                name,
                version,
                categories {
                    name,
                    children {
                        name,
                        classId,
                        children {
                            name,
                            classId,
                            children {
                                name,
                                classId
                            }
                        }
                    }
                }
            }
        }
        """

        query_variables = {
            "orgId": orgId,
            "name": name,
            "version": version,
        }
        query = dict(query=query_string, variables=query_variables)
        result = self._execute_query(query)

        Tax = Taxonomy2(remote_tax=result["taxonomy"])
        return Tax

    def get_members(self, org_id) -> Dict[Any, Any]:
        """Return all members in the organization."""
        query_string = """
        query($orgId: UUID!) {
            members(orgId: $orgId) {
                userId,
                user {
                    givenName,
                    familyName,
                    email
                }
            }
        }
        """

        query_variables = {
            "orgId": org_id,
        }
        query = dict(query=query_string, variables=query_variables)
        result = self._execute_query(query)

        # create a member map
        member_map = {}
        for member in result["members"]:
            member_map[member["userId"]] = member["user"]["email"]
        return member_map

    def _execute_query(self, query: Dict[Any, Any]) -> Any:
        """Execute a graphql query."""
        headers = {"ApiKey": self.client.api_key}
        try:
            response = requests.post(self.url, headers=headers, json=query)
            res = {}
            if "errors" in response.json():
                raise ValueError(response.json()["errors"][0]["message"])
            elif "data" in response.json():
                res = response.json()["data"]
            else:
                res = response.json()
            return res
        except ValueError:
            # print(response.content)
            # print(response.status_code)
            raise
