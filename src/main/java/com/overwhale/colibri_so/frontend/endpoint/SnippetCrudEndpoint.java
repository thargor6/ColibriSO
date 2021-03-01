package com.overwhale.colibri_so.frontend.endpoint;



import com.overwhale.colibri_so.frontend.dto.IntentDto;
import com.overwhale.colibri_so.frontend.dto.ProjectDto;
import com.overwhale.colibri_so.frontend.dto.SnippetDto;
import com.overwhale.colibri_so.frontend.dto.TagDto;
import com.overwhale.colibri_so.frontend.mapper.IntentMapper;
import com.overwhale.colibri_so.frontend.mapper.ProjectMapper;
import com.overwhale.colibri_so.frontend.mapper.SnippetMapper;
import com.overwhale.colibri_so.frontend.mapper.TagMapper;
import com.overwhale.colibri_so.frontend.service.SnippetService;
import com.vaadin.flow.server.connect.EndpointExposed;
import com.vaadin.flow.server.connect.auth.AnonymousAllowed;
import org.springframework.data.domain.Page;
import org.vaadin.artur.helpers.GridSorter;
import org.vaadin.artur.helpers.PagingUtil;

import java.util.List;
import java.util.UUID;

@AnonymousAllowed
@EndpointExposed
public abstract class SnippetCrudEndpoint extends CrudEndpoint<SnippetDto, UUID>{

    protected SnippetService getSnippetService() {
        return (SnippetService) getService();
    }

    public int countForProjectId(String projectId) {
        return getSnippetService().countForProjectId(projectId);
    }

    public List<SnippetDto> listForProjectId(String projectId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<SnippetDto> page =
                getSnippetService().listForProjectId(projectId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder)).map(e -> SnippetMapper.INSTANCE.entityToDto(e));
        return page.getContent();
    }

    public List<ProjectDto> listProjectsForSnippetId(String snippetId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<ProjectDto> page =
                getSnippetService().listProjectsForSnippetId(snippetId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder)).map(e -> ProjectMapper.INSTANCE.entityToDto(e));
        return page.getContent();
    }

    public List<TagDto> listTagsForSnippetId(String snippetId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<TagDto> page =
                getSnippetService().listTagsForSnippetId(snippetId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder)).map(e -> TagMapper.INSTANCE.entityToDto(e));
        return page.getContent();
    }

    public List<IntentDto> listIntentsForSnippetId(String snippetId, int offset, int limit, List<GridSorter> sortOrder) {
        Page<IntentDto> page =
                getSnippetService().listIntentsForSnippetId(snippetId, PagingUtil.offsetLimitTypeScriptSortOrdersToPageable(offset, limit, sortOrder)).map(e -> IntentMapper.INSTANCE.entityToDto(e));
        return page.getContent();
    }
}
