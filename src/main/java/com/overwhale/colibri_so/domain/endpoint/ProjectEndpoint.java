package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.Project;
import com.overwhale.colibri_so.domain.service.ProjectService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class ProjectEndpoint extends CrudEndpoint<Project, UUID> {
    private final ProjectService service;

    public ProjectEndpoint(@Autowired ProjectService service) {
        this.service = service;
    }

    @Override
    protected ProjectService getService() {
        return service;
    }
}