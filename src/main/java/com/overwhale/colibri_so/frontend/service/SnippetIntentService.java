package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.SnippetIntent;
import com.overwhale.colibri_so.backend.repository.SnippetIntentRepository;
import com.overwhale.colibri_so.frontend.dto.SnippetIntentDto;
import com.overwhale.colibri_so.frontend.mapper.SnippetIntentMapper;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.Optional;
import java.util.UUID;

@Service
public class SnippetIntentService extends CrudService<SnippetIntentDto, UUID> {
  private final SnippetIntentRepository repository;
  private final SnippetIntentMapper snippetIntentMapper;

  public SnippetIntentService(SnippetIntentRepository repository, SnippetIntentMapper snippetIntentMapper) {
    this.repository = repository;
    this.snippetIntentMapper = snippetIntentMapper;
  }

  public SnippetIntentDto update(SnippetIntentDto dto) {
    SnippetIntent entity = snippetIntentMapper.dtoToEntiy(dto);
    return snippetIntentMapper.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<SnippetIntentDto, UUID> getRepository() {
    return null;
  }

  public Optional<SnippetIntentDto> get(UUID id) {
    return repository.findById(id).map(e -> snippetIntentMapper.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<SnippetIntentDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> snippetIntentMapper.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
