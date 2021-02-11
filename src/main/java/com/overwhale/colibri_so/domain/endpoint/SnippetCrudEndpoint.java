package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.Snippet;
import com.overwhale.colibri_so.domain.service.SnippetService;
import com.vaadin.flow.server.connect.EndpointExposed;
import com.vaadin.flow.server.connect.auth.AnonymousAllowed;
import org.springframework.data.domain.Page;
import org.vaadin.artur.helpers.CrudService;
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
}
