package com.overwhale.colibri_so.domain.service;


import com.overwhale.colibri_so.domain.entity.SnippetProject;
import com.overwhale.colibri_so.domain.entity.SnippetTag;
import com.overwhale.colibri_so.domain.repository.SnippetProjectRepository;
import com.overwhale.colibri_so.domain.repository.SnippetTagRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.UUID;

@Service
public class SnippetTagService extends CrudService<SnippetTag, UUID> {
  private final SnippetTagRepository repository;

  public SnippetTagService(@Autowired SnippetTagRepository repository) {
    this.repository = repository;
  }

  @Override
  protected SnippetTagRepository getRepository() {
    return repository;
  }
}
