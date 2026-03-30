"""Google Tag Manager version and publishing tools."""

from typing import Any, Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_tagmanager_service, resolve_workspace_path


@mcp.tool()
def gtm_create_version(
    name: str,
    account_id: Optional[str] = None,
    container_id: Optional[str] = None,
    workspace_id: str = "Default Workspace",
    notes: str = "",
) -> dict[str, Any]:
    """Creates a new container version from the current workspace state.

    A version is a snapshot of all tags, triggers, and variables in the
    workspace. You must create a version before publishing.

    Args:
        name: Version name (e.g. "v42 - Added purchase tracking").
        account_id: GTM account ID. Uses default if not provided.
        container_id: GTM container ID. Uses default if not provided.
        workspace_id: Workspace ID. Defaults to "Default Workspace".
        notes: Optional version notes/description.

    Returns:
        dict: Version details with containerVersionId, name, path, and
            counts of tags/triggers/variables included.
    """
    try:
        workspace_path = resolve_workspace_path(account_id, container_id, workspace_id)
        service = get_tagmanager_service()

        body = {
            "name": name,
            "notes": notes,
        }

        result = service.accounts().containers().workspaces().create_version(
            path=workspace_path, body=body
        ).execute()

        version = result.get("containerVersion", {})
        return {
            "containerVersionId": version.get("containerVersionId"),
            "name": version.get("name"),
            "path": version.get("path"),
            "notes": version.get("notes", ""),
            "tagCount": len(version.get("tag", [])),
            "triggerCount": len(version.get("trigger", [])),
            "variableCount": len(version.get("variable", [])),
            "fingerprint": version.get("fingerprint"),
            "compilerError": result.get("compilerError"),
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Failed to create version: {e}") from e


@mcp.tool()
def gtm_publish_version(
    version_path: str,
) -> dict[str, Any]:
    """Publishes a container version, making it live on the website.

    This pushes all tags, triggers, and variables in the version to
    production. Changes take effect within minutes.

    WARNING: This affects your live website immediately. Make sure
    you've tested the version in GTM's preview mode first.

    Args:
        version_path: Full version path
            (e.g. "accounts/123/containers/456/versions/789").

    Returns:
        dict: Published version details with containerVersionId, name,
            and publication timestamp.
    """
    try:
        service = get_tagmanager_service()
        result = service.accounts().containers().versions().publish(
            path=version_path
        ).execute()

        version = result.get("containerVersion", {})
        return {
            "containerVersionId": version.get("containerVersionId"),
            "name": version.get("name"),
            "path": version.get("path"),
            "publishedAt": version.get("fingerprint"),
            "status": "published",
        }
    except Exception as e:
        raise ToolError(f"Failed to publish version: {e}") from e


@mcp.tool()
def gtm_list_versions(
    account_id: Optional[str] = None,
    container_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists container version headers (summaries) for a GTM container.

    Returns version summaries without full tag/trigger details.
    Use this to find version IDs for publishing.

    Args:
        account_id: GTM account ID. Uses default if not provided.
        container_id: GTM container ID. Uses default if not provided.

    Returns:
        list[dict]: List of version summaries with containerVersionId,
            name, numTags, numTriggers, numVariables, and path.
    """
    try:
        from .client import get_default_account_id, get_default_container_id

        if not account_id:
            account_id = get_default_account_id()
        if not account_id:
            raise ToolError("No account_id provided and no default configured.")

        if not container_id:
            container_id = get_default_container_id()
        if not container_id:
            raise ToolError("No container_id provided and no default configured.")

        service = get_tagmanager_service()
        parent = f"accounts/{account_id}/containers/{container_id}"
        result = service.accounts().containers().version_headers().list(
            parent=parent
        ).execute()
        headers = result.get("containerVersionHeader", [])
        return [
            {
                "containerVersionId": h.get("containerVersionId"),
                "name": h.get("name", ""),
                "numTags": h.get("numTags", "0"),
                "numTriggers": h.get("numTriggers", "0"),
                "numVariables": h.get("numVariables", "0"),
                "path": h.get("path"),
                "deleted": h.get("deleted", False),
            }
            for h in headers
        ]
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Failed to list versions: {e}") from e
