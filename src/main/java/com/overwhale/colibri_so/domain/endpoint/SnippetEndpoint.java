package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.Snippet;
import com.overwhale.colibri_so.domain.service.SnippetService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class SnippetEndpoint extends CrudEndpoint<Snippet, UUID> {
    private final SnippetService service;

    public SnippetEndpoint(@Autowired SnippetService service) {
        this.service = service;
    }

    @Override
    protected SnippetService getService() {
        return service;
    }
}
