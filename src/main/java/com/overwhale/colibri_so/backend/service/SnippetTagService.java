package com.overwhale.colibri_so.backend.service;


import com.overwhale.colibri_so.backend.entity.SnippetTag;
import com.overwhale.colibri_so.backend.repository.SnippetTagRepository;
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
