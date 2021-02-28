package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.backend.entity.Project;
import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.backend.service.SnippetService;
import com.vaadin.flow.server.connect.EndpointExposed;
import com.vaadin.flow.server.connect.auth.AnonymousAllowed;
import org.springframework.data.domain.Page;
import org.vaadin.artur.helpers.GridSorter;
import org.vaadin.artur.helpers.PagingUtil;

import java.util.List;
import java.util.UUID;

@AnonymousAllowed
@EndpointExposed
public abstract class SnippetCrudEndpoint extends CrudEndpoint<Snippet, UUID>{

    protected SnippetService getSnippetService() {
        return (SnippetService) getService();
    }

    public int countForProjectId(String projectId) {
        return getSnippetService().countForProjectId(projectId);
    }

    public List<Snippet> listForProjectId(String projectId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<Snippet> page =
                getSnippetService().listForProjectId(projectId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder));
        return page.getContent();
    }

    public List<Project> listProjectsForSnippetId(String snippetId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<Project> page =
                getSnippetService().listProjectsForSnippetId(snippetId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder));
        return page.getContent();
    }

    public List<Tag> listTagsForSnippetId(String snippetId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<Tag> page =
                getSnippetService().listTagsForSnippetId(snippetId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder));
        return page.getContent();
    }

    public List<Intent> listIntentsForSnippetId(String snippetId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<Intent> page =
                getSnippetService().listIntentsForSnippetId(snippetId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder));
        return page.getContent();
    }
}
